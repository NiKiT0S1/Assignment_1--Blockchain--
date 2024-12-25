# Assignment 1

This project demonstrates a basic blockchain implementation in Python. The implementation does not rely on any external libraries and showcases simplified hashing, a Merkle tree, and mechanisms for mining and validating blocks.

---

## Features

### 1. Custom Hashing Algorithm
- Implements a simplified version of SHA-256 without external libraries.
- Ensures secure hashing for each block and Merkle root.

### 2. Merkle Tree
- Computes the Merkle root for a set of 10 transactions in each block.
- Provides an efficient and secure method to validate transactions.

### 3. Blockchain Structure
Each block contains:
- Previous block's hash
- Timestamp
- Merkle root (calculated from 10 transactions)
- Nonce (for proof-of-work)
- Current block hash

### 4. Mining and Validation
- Blocks are mined by finding a hash that satisfies a given difficulty level (number of leading zeros).
- Blockchain integrity is ensured through validation of hashes and block linkage.

---

## Code Overview

### 1. Hashing Algorithm
The custom hashing function is a simplified version of SHA-256 that processes input data into a fixed-length hash using mathematical operations.

```python
# Simplified SHA-256

def hash(text):
    def rotate_right(x, n):
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    def sha256_compression(chunk, h):
        # SHA-256 constants and compression logic
        ...

    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]

    # Padding and chunk processing logic
    ...

    return ''.join(f'{value:08x}' for value in h)
```

### 2. Merkle Tree
The Merkle tree recursively calculates hashes for pairs of transactions until a single root hash is derived.

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

### 3. Block Class
Represents a single block in the blockchain, containing transactions, timestamps, and mining logic.

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

### 4. Blockchain Class
Manages the blockchain structure, mining, and validation of blocks.

```python
class Blockchain:
    def __init__(self, difficulty=4):
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

### 5. Main Execution
Predefined transactions are added, blocks are mined, and the blockchain's integrity is validated.

```python
if __name__ == "__main__":
    blockchain = Blockchain()

    transactions_1 = [...]
    transactions_2 = [...]

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

---

## Output
- Displays details of each block, including hashes, transactions, and Merkle roots.
- Indicates whether the blockchain is valid.

---

## Customization
- Adjust mining difficulty by modifying the `difficulty` parameter in the `Blockchain` constructor.
- Add or modify transactions to test blockchain functionality.

