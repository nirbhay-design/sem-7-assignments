from gettext import find
import hashlib, json, copy
from ecdsa import SigningKey
import datetime, random, time

def find_hash(text):
    m = hashlib.sha256()
    m.update(text.encode())
    return m.hexdigest()

class Utxo:
    def __init__(self,hash_pub):
        self.unspend_trans = [] # array of dict ([{"from":hash_pubkey,"to":hash_pubkey,"btc":int}])
        self.hash_pub = hash_pub    

    def add_transaction(self,transaction):
        # transaction is {"from","to","btc"}
        self.unspend_trans.append(transaction)
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
    def __init__(self):
        self.sk, self.pk = self.generate_private_public()
        self.hash = find_hash(self.pk.to_string().hex())
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
    def __init__(self):
        self.w = wallet()
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
        self.transaction_hash = [self.transactions[i]['hash'] for i in range(len(self.transactions))]
        self.merkle_hash = self.merkle_tree(self.transaction_hash)

    def calculate_hash(self, nonce):
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
            print(f"{'#'*5} transaction {idx} details {'#'*5}")
            print(f"transaction id: {transaction['id']}")
            print(f"transaction hash: {transaction['hash']}")
            print(f"{transaction['from']} -> {transaction['to']}, btc: {transaction['btc']}, fees: {transaction['fees']}")
        print('\n')

class miner:
    def __init__(self,*args):
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
        self.miner_wallet = wallet()
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

class blockchain:
    def __init__(self,n_miners = 10, n_users=20):
        self.n_miners = n_miners
        self.user_list = []
        self.miner_list = []
        for i in range(n_users):
            self.user_list.append(users())
        for i in range(n_miners):
            ith_miner = miner(self.user_list[2*i], self.user_list[2*i+1])
            self.miner_list.append(ith_miner)
            self.user_list[2*i].miner_connection(ith_miner)
            self.user_list[2*i+1].miner_connection(ith_miner)
        for i in range(n_miners):
            self.miner_list[i].miner_neighbour(*(self.miner_list[:i]+self.miner_list[i+1:]))

        # add some initial transactions to utxo;
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
    blockc = blockchain()

    while 1:
        print("choices: ")
        print("0 for doing transaction")
        print("1 for printing blockchain")
        print("2 for printing utxo for specific user")
        print('3 for printing utxo for specific miner')
        print("4 for exiting")


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
            break
