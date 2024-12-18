import time

# HASHING ALGORITHM (SHA-256 simplified without libraries)
def hash(data):
    hash_value = 0
    for char in data:
        hash_value = (hash_value * 31 + ord(char)) % (2 ** 32)
    return format(hash_value, '08x')

# MERKLE TREE
def merkle_root(transactions):
    if len(transactions) == 1:
        return hash(transactions[0])

    new_level = []
    for i in range(0, len(transactions), 2):
        left = transactions[i]
        if i + 1 < len(transactions):
            right = transactions[i + 1]
        else:
            right = transactions[i]
        new_level.append(hash(left + right))

    return merkle_root(new_level)

# EACH BLOCK
class Block:
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.merkle_root = merkle_root(transactions)
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}"
        return hash(block_data)

    def mine_block(self, difficulty):
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()

# BLOCKCHAIN IMPLEMENTATION
class Blockchain:
    def __init__(self, difficulty = 0):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("0", ["Genesis Block"])
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        if len(transactions) != 10:
            raise ValueError("Each block must contain exactly 10 transactions.")
        previous_hash = self.chain[-1].hash
        new_block = Block(previous_hash, transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# TEST BLOCKCHAIN
if __name__ == "__main__":
    blockchain = Blockchain()

    transactions_1 = [
        "Alice->Bob:10",
        "Bob->Charlie:5",
        "Charlie->Dave:7",
        "Dave->Eve:3",
        "Eve->Frank:8",
        "Frank->Grace:2",
        "Grace->Heidi:1",
        "Heidi->Ivan:6",
        "Ivan->Judy:4",
        "Judy->Alice:9"
    ]

    transactions_2 = [
        "Tom->Jerry:15",
        "Jerry->Spike:20",
        "Spike->Tyke:25",
        "Tyke->Butch:30",
        "Butch->Tom:35",
        "Tom->Nibbles:40",
        "Nibbles->Quacker:45",
        "Quacker->Droopy:50",
        "Droopy->Slick:55",
        "Slick->Tom:60"
    ]

    blockchain.add_block(transactions_1)
    blockchain.add_block(transactions_2)

    for i, block in enumerate(blockchain.chain):
        print(f"Block {i}:")
        print(f" Previous Hash: {block.previous_hash}")
        print(f" Transactions: {block.transactions}")
        print(f" Merkle Root Hash: {block.merkle_root}")
        print(f" Hash: {block.hash}\n")

    print("Is the blockchain correct?", blockchain.validate_blockchain())