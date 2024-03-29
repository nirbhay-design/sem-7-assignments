from gettext import find
import hashlib, json, copy
from ecdsa import SigningKey
import datetime, random, time
import sqlite3, sys

class database(object):
    def __init__(self, database_table):
        self.con = sqlite3.connect(database_table)
        self.cursor = self.con.cursor()

    def run(self,query):
        self.cursor.execute(query)
        self.con.commit()

    def fetch(self, query):
        return self.cursor.execute(query)

sql_db = database(sys.argv[1])

def create_database(queries):
    for query in queries:
        sql_db.run(query)

def find_hash(text):
    m = hashlib.sha256()
    m.update(text.encode())
    return m.hexdigest()

class Utxo:
    def __init__(self,hash_pub):
        self.unspend_trans = [] # array of dict ([{"id", "from":hash_pubkey, "to":hash_pubkey, "btc":int}])
        res = sql_db.fetch(f"select utxohash, utxos from userpk where pubkeyhash = '{hash_pub}'").fetchall()
        if res:
            for utxhash, utx in res:
                self.unspend_trans.append(json.loads(utx))
        self.hash_pub = hash_pub    

    def add_transaction(self,transaction):
        # transaction is {"from","to","btc"}
        self.unspend_trans.append(transaction)
        transaction_msg = transaction['from'] + transaction['to'] + str(transaction['btc']) + self.hash_pub + str(random.randint(0,1e4))
        utxo_tran_hash = find_hash(transaction_msg)
        transaction['id'] = utxo_tran_hash
        sql_db.run(f"insert into userpk values ('{self.hash_pub}', '{utxo_tran_hash}', '{json.dumps(transaction)}')")
        self.unspend_trans = sorted(self.unspend_trans, key=lambda x:x['btc'],reverse=True)
    
    def utxotransaction(self,amount):
        filtered_utxo = []
        removed_utxo = []
        overflow = 0
        for utxos in self.unspend_trans:
            cur_btc = utxos['btc']
            if amount <= 0:
                filtered_utxo.append(utxos)
                continue
            else:
                removed_utxo.append(utxos)    
            amount -= cur_btc;
            if amount < 0:
                overflow = -amount
        
        if amount <= 0:
            self.unspend_trans = copy.deepcopy(filtered_utxo)
            for removed_transaction in removed_utxo:
                tran_id = removed_transaction['id']
                sql_db.run(f"delete from userpk where utxohash = '{tran_id}'")
        else:
            # print(f'transaction amount {amount}, Not enough BTC')
            self.unspend_trans = copy.deepcopy(removed_utxo)

        if overflow:
            self.add_transaction({"from":self.hash_pub,"to":self.hash_pub,"btc":overflow})

    def is_transaction_possible(self,amount):
        for utxos in self.unspend_trans:
            cur_btc = utxos['btc']
            amount -= cur_btc;
            if amount <= 0:
                return True  
        
        return False
        
    def show_utxo(self):
        for i in self.unspend_trans:
            print(f"{i['from']} -> {i['to']} {i['btc']} btc")

class wallet:
    """
    each user will have a wallet which contains the utxo and contains 
    the public key and private key and wallet hash is hash of public key
    """
    def __init__(self, idx, miner=False):
        self.idx = idx

        if not miner:
            res = sql_db.fetch(f"select prkey from userprk where user_idx = {self.idx}")
        else:
            res = sql_db.fetch(f"select prkey from minerprk where miner_idx = {self.idx}")

        data = res.fetchall()

        if len(data) == 0:
            self.sk, self.pk = self.generate_private_public()
            hex_private_key = self.sk.to_string().hex()
            hex_pub_key = self.pk.to_string().hex()
            if miner:
                sql_db.run(f"insert into minerprk values ('{self.idx}', '{hex_private_key}', '{find_hash(hex_pub_key)}')")
            else:
                sql_db.run(f"insert into userprk values ('{self.idx}', '{hex_private_key}', '{find_hash(hex_pub_key)}')")

        else:
            private_key = data[0][0]
            byte = bytes()
            byte_key = byte.fromhex(private_key)
            self.sk = SigningKey.from_string(byte_key)
            self.pk = self.sk.verifying_key

        self.hash = find_hash(self.pk.to_string().hex())
        self.hexsk = self.sk.to_string().hex()
        self.utxo = Utxo(self.hash)


    def generate_private_public(self):
        sk = SigningKey.generate() # uses NIST192p
        pk = sk.verifying_key
        return sk, pk
        # signature = sk.sign(b"message")
        # vk.verify(signature, b"message")
    def sign_transaction(self,transaction:dict, user_idx: int):
        # for to
        is_transaction_possible = self.utxo.is_transaction_possible(transaction['btc']+transaction['fees'])
        if is_transaction_possible:
            transaction_message = transaction['from']+transaction['to']+str(transaction['btc'])+str(transaction['fees'])
            transaction_hash = find_hash(transaction_message)
            transaction_signature = self.sk.sign(transaction_hash.encode()).hex()
        else:
            # print("transaction not possible")
            return  


        transaction_id = find_hash(transaction_message+str(user_idx))
        signaturized_transaction = {**transaction, "sign":transaction_signature, "hash":transaction_hash, "id": transaction_id}
        return signaturized_transaction

    def update_utxo(self, transaction_btc):
        self.utxo.utxotransaction(transaction_btc)

    def add_utxo(self, transaction):
        self.utxo.add_transaction(transaction)

    def show_wallet(self):
        print("address: ", self.hash)

    def show_utxo(self):
        self.utxo.show_utxo()

class users:
    def __init__(self, idx):
        self.w = wallet(idx)
        self.connected_miner = []

    def pkhash(self):
        return self.w.hash

    def pk(self):
        return self.w.pk

    def miner_connection(self, miner_connected):
        self.connected_miner.append(miner_connected)


class block:
    def __init__(self,**kwargs):
        self.block_no = kwargs['block_no']
        self.timestamp = kwargs['timestamp']
        self.prev_hash = kwargs["prev_hash"]
        self.nonce = None
        self.cur_hash = None
        self.transactions = kwargs['transactions']
        self.transaction_hash = None
        self.merkle_hash = None

    def calculate_hash(self, nonce):
        self.transaction_hash = [self.transactions[i]['hash'] for i in range(len(self.transactions))]
        self.merkle_hash = self.merkle_tree(self.transaction_hash) if self.merkle_hash is None else self.merkle_hash
        self.nonce = nonce
        concat_string = str(self.block_no) + self.timestamp + self.prev_hash + str(self.nonce) + "".join(self.transaction_hash) + self.merkle_hash
        self.cur_hash = find_hash(concat_string)
        return self.cur_hash 

    def merkle_tree(self, transaction_list: list):
        cur_list = [i for i in transaction_list]
        while len(cur_list) != 1:
            hash_layer = []
            cur_len = len(cur_list) // 2
            for i in range(cur_len):
                if (2*i + 1 == len(cur_list)):
                    hash_layer.append(cur_list[2*i])
                else:
                    hash_layer.append(find_hash(cur_list[2*i] + cur_list[2*i + 1]))
            cur_list = copy.deepcopy(hash_layer)
        
        return cur_list[0]

    def show_block(self):
        print(f"\nblock_no: {self.block_no}")
        print(f"timestamp: {self.timestamp}")
        print(f"nonce: {self.nonce}")
        print(f"prev_hash: {self.prev_hash}")
        print(f"cur_hash: {self.cur_hash}")
        print(f"merkle_root_hash: {self.merkle_hash}")
        print(f"----- Transactions -----")
        for idx, transaction in enumerate(self.transactions):
            print(f"transaction hash: {transaction['hash']}")
        print('\n')

class miner:
    def __init__(self,idx,*args):
        self.user_neighbors = []
        self.miner_neighbors = []
        for user_miner in args:
            if isinstance(user_miner,users):
                self.user_neighbors.append(user_miner)
            elif isinstance(user_miner,miner):
                self.miner_neighbors.append(user_miner)
            else:
                print("invalid neighbor argument")
        
        self.blockchain = []
        self.mempool = {}
        self.miner_wallet = wallet(idx, miner=True)
        self.max_nonce = int(1e8)

    def miner_neighbour(self,*args):
        for user_miner in args:
            if isinstance(user_miner,miner):
                self.miner_neighbors.append(user_miner)
            else:
                print("invalid neighbor argument")

    def validate_transaction(self, signaturized_transaction: dict, from_user: users):
        # transaction contains {from, to, btc, sign}
            transaction_message = signaturized_transaction['from']+signaturized_transaction['to']+str(signaturized_transaction['btc']) + str(signaturized_transaction['fees'])
            transaction_hash = find_hash(transaction_message)
            byt = bytes()
            byte_sign = byt.fromhex(signaturized_transaction['sign'])
            try:
                transaction_verify = from_user.pk().verify(byte_sign,transaction_hash.encode())
            except Exception as e:
                print(e)
                return False
            return transaction_verify

    def add_to_mempool(self, transaction):
        self.mempool[transaction['id']] = transaction

    def update_mempool(self):
        cur_mempool_transaction_id = list(self.mempool.keys())
        self.mempool = {}
        for idx in range(len(self.miner_neighbors)):
            for tran_id in cur_mempool_transaction_id:
                self.miner_neighbors[idx].mempool.pop(tran_id)
                # print(f"updated miner {idx} mempool {self.miner_neighbors[idx].mempool}")

    def propogate_to_othermempools(self):
        for idx in range(len(self.miner_neighbors)):
            self.miner_neighbors[idx].mempool = copy.deepcopy(self.mempool)

    def mine_block(self, transaction_list: list):
        # transaction_list contains the hashes of all the transactions
        if self.blockchain:
            new_block = block(
                    block_no = len(self.blockchain),
                    timestamp = str(datetime.datetime.now()),
                    prev_hash = self.blockchain[-1].cur_hash,
                    transactions = transaction_list,
                    starting_nonce = 0
                )
        else:
            new_block = block(
                    block_no = len(self.blockchain),
                    timestamp = str(datetime.datetime.now()),
                    prev_hash = "0",
                    transactions = transaction_list,
                    starting_nonce = 0
                )

        mine_successful = False
        for i in range(self.max_nonce):
            cur_block_hash = new_block.calculate_hash(i)
            if cur_block_hash[:4] == "0000":
                mine_successful = True
                break
            else:
                new_block.timestamp = str(datetime.datetime.now())
        
        if mine_successful:
            print(new_block.cur_hash)
            self.blockchain.append(new_block)
        else:
            print('nonce exhausted')

    def pass_blockchain(self):
        for miner_idx in range(len(self.miner_neighbors)):
            self.miner_neighbors[miner_idx].blockchain = copy.deepcopy(self.blockchain)

    def show_mempool(self):
        for tran_id in self.mempool.values():
            print(tran_id)

def reconstruct_blockchain():
    cons_blockchain = []
    block_chn = {}
    res = sql_db.fetch("select * from (block inner join transactions on block.tranhash = transactions.tranhash)").fetchall()
    if res:
        for blockhash, prevhash, timestamp, merkle, tranhash, blht, nonce, thash, from_id, to_id, btc, fees, miner_ch in res:
            transaction_cur = {'hash':tranhash,'from':from_id,'to':to_id,"btc":btc,"fees":fees}            
            if block_chn.get(blockhash, -1) == -1:
                nblock = block(
                    block_no = blht,
                    timestamp = timestamp,
                    prev_hash = prevhash,
                    transactions = [transaction_cur]
                )
                nblock.nonce = nonce
                nblock.cur_hash = blockhash
                nblock.merkle_hash = merkle
                block_chn[blockhash] = nblock
            else:
                block_chn[blockhash].transactions.append(transaction_cur)
        for key,value in block_chn.items():
            cons_blockchain.append(value)

    return cons_blockchain

class blockchain:
    def __init__(self,n_miners = 10, n_users=20):
        self.blc = reconstruct_blockchain()
        self.n_miners = n_miners
        self.user_list = []
        self.miner_list = []
        for i in range(n_users):
            self.user_list.append(users(i))
        for i in range(n_miners):
            ith_miner = miner(i,self.user_list[2*i], self.user_list[2*i+1])
            ith_miner.blockchain = copy.deepcopy(self.blc)
            self.miner_list.append(ith_miner)
            self.user_list[2*i].miner_connection(ith_miner)
            self.user_list[2*i+1].miner_connection(ith_miner)
        for i in range(n_miners):
            self.miner_list[i].miner_neighbour(*(self.miner_list[:i]+self.miner_list[i+1:]))

        # add some initial transactions to utxo;
        ref = sql_db.fetch('select count(*) from userpk').fetchall()[0][0]
        if not ref:
            for i in range(n_users):
                self.user_list[i].w.add_utxo({"from":self.user_list[random.randint(0,n_users-1)].pkhash(),"to":self.user_list[i].pkhash(),'btc':3})
                self.user_list[i].w.add_utxo({"from":self.user_list[random.randint(0,n_users-1)].pkhash(),"to":self.user_list[i].pkhash(),'btc':50})
                self.user_list[i].w.add_utxo({"from":self.user_list[random.randint(0,n_users-1)].pkhash(),"to":self.user_list[i].pkhash(),'btc':1})
                self.user_list[i].w.add_utxo({"from":self.user_list[random.randint(0,n_users-1)].pkhash(),"to":self.user_list[i].pkhash(),'btc':10})

        self.transaction_database = {}

    def transaction(self, transactions):
        transactions_list = []
        all_transactions = []
        not_verified_transaction = []
        user_amount_deduct = {}
        for idx, (from_idx, to_idx, btc, fees) in enumerate(transactions):
            transact = self.generate_transaction(from_idx, to_idx, btc, fees)
            all_transactions.append(transact)
            
            if user_amount_deduct.get(from_idx, -1) == -1:
                signed_transaction = self.user_list[from_idx].w.sign_transaction(transact, from_idx)
            else:
                signed_transaction = self.user_list[from_idx].w.sign_transaction(transact, user_amount_deduct[from_idx] + fees)
            
            if signed_transaction is None:
                print(f'transaction ({from_idx} {to_idx} {btc} {fees}) not possible')
                not_verified_transaction.append(idx)
                continue
            
            if (user_amount_deduct.get(from_idx, -1)):
                user_amount_deduct[from_idx] = (fees + transact['btc'])
            else:
                user_amount_deduct[from_idx] += (fees + transact['btc'])

            verification = self.verify_transaction(signed_transaction, from_idx) # verify transaction by all miners
            if not verification:
                print("transaction not verified")
                return False

            transactions_list.append(signed_transaction)
            self.transaction_database[signed_transaction['hash']] = signed_transaction
            self.user_list[from_idx].connected_miner[0].add_to_mempool(signed_transaction)
            self.user_list[from_idx].connected_miner[0].propogate_to_othermempools()

        if not transactions_list:
            return False

        # randomly select a miner to do the mining
        chosen_miner, _ = self.proof_of_work()
        print("miner chosen: ", chosen_miner)
        miner_selected = self.miner_list[chosen_miner]
        miner_selected.pass_blockchain()
        miner_selected.update_mempool()

        last_block_mined = miner_selected.blockchain[-1]
        for i in range(len(last_block_mined.transactions)):
            curtransact = last_block_mined.transactions[i]
            sql_db.run(f"insert into transactions values ('{curtransact['hash']}', '{curtransact['from']}', '{curtransact['to']}', '{curtransact['btc']}', '{curtransact['fees']}', {chosen_miner})")
            sql_db.run(f"insert into block values ('{last_block_mined.cur_hash}', '{last_block_mined.prev_hash}', '{last_block_mined.timestamp}', '{last_block_mined.merkle_hash}', '{last_block_mined.transaction_hash[i]}', {last_block_mined.block_no}, {last_block_mined.nonce})")

        for idx, (from_idx, to_idx, btc, fees) in enumerate(transactions):
            if idx not in not_verified_transaction:
                transact = all_transactions[idx]
                self.user_list[from_idx].w.update_utxo(transact['btc']+transact['fees'])
                self.user_list[to_idx].w.add_utxo(transact)
                self.miner_list[chosen_miner].miner_wallet.add_utxo(
                    {
                        'from': self.user_list[from_idx].pkhash(), 
                        "to":self.miner_list[chosen_miner].miner_wallet.hash,
                        'btc': fees
                    }
                )

        return True

    def proof_of_work(self):
        time_list = []
        for idx in range(len(self.miner_list)):
            time1 = time.perf_counter();
            cur_miner = self.miner_list[idx]
            mempool_transactions = list(cur_miner.mempool.values())
            cur_miner.mine_block(mempool_transactions)
            time2 = time.perf_counter();
            time_list.append((idx,time2 - time1))
        # print(time_list)
        return min(time_list, key=lambda x:x[1])
        
    def verify_transaction(self, transaction, from_idx):
        verify = True
        for mine in self.miner_list:
            verify &= mine.validate_transaction(transaction, self.user_list[from_idx])

        return verify

    def generate_transaction(self, from_idx: int, to_idx: int, btc: int, fees: int):
        transact = {"from":self.user_list[from_idx].pkhash(), "to":self.user_list[to_idx].pkhash(), "btc": btc, "fees":fees}
        return transact

    def show_user_utxo(self, user_idx):
        self.user_list[user_idx].w.show_utxo()

    def show_miner_utxo(self, miner_idx):
        self.miner_list[miner_idx].miner_wallet.show_utxo()

    def show_miner_mempool(self, miner_idx):
        self.miner_list[miner_idx].show_mempool()

    def show_blockchain(self):
        for block in self.miner_list[0].blockchain:
            block.show_block()

    def show_connection(self):
        for idx, mine in enumerate(self.miner_list):
            print(idx)

            for user_neighbors in mine.user_neighbors:
                print(user_neighbors.pkhash())

            for miner_neighbors in mine.miner_neighbors:
                print(miner_neighbors.miner_wallet.hash)

    def show_user(self):
        for idx, user in enumerate(self.user_list):
            print(f"{idx} -> {user.pkhash()}")

    def show_miner(self):
        for idx, mine in enumerate(self.miner_list):
            print(f"{idx} -> {mine.miner_wallet.hash}")

    def show_transactions(self):
        print(self.transaction_database)

if __name__ == "__main__":

    query1 = """
        create table if not exists block (
            blockhash varchar,
            prevhash varchar,
            timestamp varchar,
            merkle varchar,
            tranhash varchar,
            blkht int,
            nonce int
        )    
    """

    query2 = """
        create table if not exists transactions (
            tranhash varchar,
            from_id varchar,
            to_id varchar,
            btc varchar,
            fees varchar,
            chosen_miner int
        )    
    """

    query3 = """
        create table if not exists userpk (
            pubkeyhash varchar,
            utxohash varchar,
            utxos varchar
        )    
    """

    query4 = """
        create table if not exists userprk (
            user_idx int,
            prkey varchar,
            pubkeyhash varchar
        )    
    """

    query5 = """
        create table if not exists minerprk (
            miner_idx int,
            prkey varchar,
            pubkeyhash varchar
        )    
    """

    queries = [query1, query2, query3, query4, query5]
    create_database(queries)
    
    blockc = blockchain()

    while 1:
        print("choices: ")
        print("0 for doing transaction")
        print("1 for printing blockchain")
        print("2 for printing utxo for specific user")
        print('3 for printing utxo for specific miner')
        print("4 for answering query1")
        print("5 for answering query2")
        print("6 for answering query3")
        print("7 for answering query4")
        print("8 for answering query5")
        print("9 for answering query6")
        print("10 for answering query7")
        print("11 for exiting")


        choice = int(input("enter your choice: "))

        if choice == 0:
            n_transactions = int(input("enter number of transactions at a time: "))
            transactions_info = []
            for trans in range(n_transactions):
                tran_info = list(map(float, input().split()))
                tran_info[0] = int(tran_info[0])
                tran_info[1] = int(tran_info[1])
                transactions_info.append(tran_info)
            blockc.transaction(transactions_info)               
        elif choice == 1:
            blockc.show_blockchain()
            # blockc.show_transactions()

        elif choice == 2:
            user_idx = int(input("enter user index: "))
            blockc.show_user_utxo(user_idx)

        elif choice == 3:
            miner_idx = int(input('enter miner index: '))
            blockc.show_miner_utxo(miner_idx)

        elif choice == 4:
            ansquery1 = """
                select distinct blockhash from block where prevhash = '0'
            """

            res = sql_db.fetch(ansquery1).fetchall()
            print("genesis block hash is :", res[0][0])

        elif choice == 5:

            ansquery2 = """
                select tranhash, btc, fees from transactions
            """

            res = sql_db.fetch(ansquery2).fetchall()
            for trid, btc, fees in res:
                print(f"id: {trid}, btc: {btc}, fees: {fees}")

        elif choice == 6:
            hash_inp = input("enter hash of block: ")
            ansquery3 = f"select * from block where blockhash = '{hash_inp}'"

            res = sql_db.fetch(ansquery3).fetchall()
            print(f"block hash: {res[0][0]}")
            print(f"block timestamp: {res[0][2]}")
            print(f"block prev hash: {res[0][1]}")
            print(f"block nonce: {res[0][6]}")
            print(f"block merkle: {res[0][3]}")
            print(f"block height: {res[0][5]}")
            print(f"block number of transactions: {len(res)}")
            

        elif choice == 7:
            ansquery4 = f"select max(blkht) from block"

            res = sql_db.fetch(ansquery4).fetchall()
            print(f"maximum block height: {res[0][0]}")

        elif choice == 8:
            ansquery5 = f"select * from block where blkht = (select max(blkht) as recent from block)"
            res = sql_db.fetch(ansquery5).fetchall()
            print(f"block hash: {res[0][0]}")
            print(f"block timestamp: {res[0][2]}")
            print(f"block prev hash: {res[0][1]}")
            print(f"block nonce: {res[0][6]}")
            print(f"block merkle: {res[0][3]}")
            print(f"block height: {res[0][5]}")
            print(f"block number of transactions: {len(res)}")

        elif choice == 9:
            ansquery6 = f"select avg(trans_count) from (select count(tranhash) as trans_count from block group by blockhash)"
            res = sql_db.fetch(ansquery6).fetchall()
            print(f"average number of transactions: {res[0][0]}")

        elif choice == 10:
            ht = int(input("enter block height: "))
            ansquery7 = f"select count(tranhash), sum(btc) from ((select tranhash as party from block where blkht = {ht}) as new_table inner join transactions on new_table.party = transactions.tranhash)"
            res = sql_db.fetch(ansquery7).fetchall()
            print(f"number of transactions: {res[0][0]}")
            print(f"number of bitcoins: {res[0][1]}")

        elif choice == 11:
            break
