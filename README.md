# Assignment 1

This project demonstrates a basic blockchain implementation in Python without using external libraries. It includes simplified hashing, a Merkle tree, and a mechanism for mining and validating blocks.

---

## Features

1. **Custom Hashing Algorithm**:
   - Implements a simplified version of SHA-256 without relying on external libraries.
   - Ensures each block and Merkle root is securely hashed.

2. **Merkle Tree**:
   - Computes the Merkle root for a set of 10 transactions in each block.
   - Provides an efficient and secure way to validate transactions within the block.

3. **Blockchain Structure**:
   - Each block contains:
     - Previous block's hash
     - Timestamp
     - Merkle root (calculated from 10 transactions)
     - Nonce (for proof-of-work)
     - Current block hash

4. **Mining and Validation**:
   - Blocks are mined by finding a hash with a specific number of leading zeros (difficulty).
   - Blockchain integrity is validated by ensuring hashes match and blocks are correctly linked.

---

## Code

### 1. **Hashing Algorithm**
```python
# HASHING ALGORITHM (SHA-256 simplified without libraries)
def hash(data):
    hash_value = 0
    for char in data:
        hash_value = (hash_value * 31 + ord(char)) % (2 ** 32)
    return format(hash_value, '08x')
```
- Converts input data into a fixed-length hash.
- Uses a simple mathematical formula to simulate a hashing process.

### 2. **Merkle Tree**
```python
def merkle_root(transactions):
    if len(transactions) == 1:
        return hash(transactions[0])

    new_level = []
    for i in range(0, len(transactions), 2):
        left = transactions[i]
        right = transactions[i + 1] if i + 1 < len(transactions) else transactions[i]
        new_level.append(hash(left + right))

    return merkle_root(new_level)
```
- Constructs a Merkle tree from a list of transactions.
- Recursively calculates hashes until a single root is derived.

### 3. **Block Class**
```python
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
```
- Represents a single block in the blockchain.
- Computes the block's hash and supports mining with a difficulty target.

### 4. **Blockchain Class**
```python
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
```
- Manages the blockchain structure and operations.
- Includes methods to add blocks, mine them, and validate the blockchain's integrity.

### 5. **Main Execution**
```python
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
```
- Adds predefined transactions to the blockchain.
- Mines and validates the blockchain.
- Outputs details of each block and the result of the validation.

---

## Output
- Displays details for each block, including hashes, transactions, and Merkle roots.
- Confirms whether the blockchain is valid.

---

## Customization
- Adjust mining difficulty by modifying `difficulty` in the `Blockchain` constructor.
- Modify or add transactions to test the blockchain functionality.


