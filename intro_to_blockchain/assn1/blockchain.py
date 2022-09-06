from gettext import find
import hashlib
from ecdsa import SigningKey

def find_hash(text):
    m = hashlib.sha256()
    m.update(text.encode())
    return m.hexdigest()


class wallet:
    """
    each user will have a wallet which contains the utxo and contains 
    the public key and private key and wallet hash is hash of public key
    """
    def __init__(self):
        self.sk, self.pk = self.generate_private_public()
        self.utxo = []
        self.hash = find_hash(self.pk.to_string().hex())

    def generate_private_public(self):
        sk = SigningKey.generate() # uses NIST192p
        pk = sk.verifying_key
        return sk, pk
        # signature = sk.sign(b"message")
        # vk.verify(signature, b"message")

    def show_wallet(self):
        print(self.hash)
        print(self.utxo)

    def update_utxo(self, transaction):
        # transaction format (amt: int,"sender": str,"receiver":str)
        self.utxo.append(transaction)

    def transactions(self,receiver_addr, receiver_name, amount):
        self.utxo = sorted(self.utxo,key=lambda x:x[2])
        removing_index = []
        for idx, a in enumerate(self.utxo):
            if amount >= a[2]:
                amount -= a[2]
                removing_index.append(idx)
            else:
                break
        for i in removing_index:
            self.utxo.pop(i)
        
class miner:
    pass

class users:
    def __init__(self):
        pass

class block:
    pass


if __name__ == "__main__":
    w1 = wallet()
    w1.show_wallet()