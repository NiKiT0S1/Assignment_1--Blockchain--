import time


# HASHING ALGORITHM (SHA-256 simplified without libraries)
def hash(text):
    def rotate_right(x, n):
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    def sha256_compression(chunk, h):
        # Constant of SHA-256
        k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        w = [0] * 64
        for i in range(16):
            w[i] = int.from_bytes(chunk[i * 4:(i + 1) * 4], 'big')
        for i in range(16, 64):
            s0 = rotate_right(w[i - 15], 7) ^ rotate_right(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = rotate_right(w[i - 2], 17) ^ rotate_right(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h0 = h

        for i in range(64):
            S1 = rotate_right(e, 6) ^ rotate_right(e, 11) ^ rotate_right(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h0 + S1 + ch + k[i] + w[i]) & 0xFFFFFFFF
            S0 = rotate_right(a, 2) ^ rotate_right(a, 13) ^ rotate_right(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h0, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xFFFFFFFF, c, b, a, (temp1 + temp2) & 0xFFFFFFFF

        return [(x + y) & 0xFFFFFFFF for x, y in zip(h, [a, b, c, d, e, f, g, h0])]

    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    data = bytearray(text, 'utf-8')
    length = len(data) * 8
    data.append(0x80)
    while (len(data) % 64) != 56:
        data.append(0)
    data += length.to_bytes(8, 'big')

    for chunk_index in range(0, len(data), 64):
        chunk = data[chunk_index:chunk_index + 64]
        h = sha256_compression(chunk, h)

    return ''.join(f'{value:08x}' for value in h)


# MERKLE TREE
def merkle_root(transactions):
    # Function to generate the Merkle root hash from a list of transactions
    if len(transactions) == 1:
        return hash(transactions[0])

    new_level = []

    # Iterate through the transactions in pairs
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
        # Keep mining until the block's hash starts with the prefix
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()


# BLOCKCHAIN IMPLEMENTATION
class Blockchain:
    def __init__(self, difficulty=4):

        # Constructor for the Blockchain class
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block() # Create the first block (genesis block)

    def create_genesis_block(self):
        genesis_block = Block("0", ["Genesis Block"])
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block) # Add the genesis block to the blockchain like the first block

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