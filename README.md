# Assignment 1

This project demonstrates a basic blockchain implementation in Python without using external libraries. It includes simplified hashing, a Merkle tree, a mechanism for mining and validating blocks, and an integration of RSA-based digital signatures for securing transactions.

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

### 5. Digital Signatures
- Implements RSA-based digital signatures to sign and verify transactions.
- Ensures the authenticity and integrity of transactions in the blockchain.

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

### 5. RSA Digital Signature
Adds RSA-based digital signatures for signing and verifying transactions.

```python
class RSA:
    def __init__(self, p, q):
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = self.generate_e(self.phi)
        self.d = self.modinv(self.e, self.phi)

    def generate_e(self, phi):
        for e in range(2, phi):
            if math.gcd(e, phi) == 1:
                return e
        raise ValueError("No valid 'e' found")

    def modinv(self, a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        return x1 + m0 if x1 < 0 else x1

    def encrypt(self, plaintext, key):
        e, n = key
        return [pow(ord(char), e, n) for char in plaintext]

    def decrypt(self, ciphertext, key):
        d, n = key
        return ''.join(chr(pow(char, d, n)) for char in ciphertext)

    def generate_keys(self):
        return (self.e, self.n), (self.d, self.n)

def sign(private_key, document):
    e, n = private_key
    return [pow(ord(char), e, n) for char in document]

def verify(public_key, document, signature):
    d, n = public_key
    decrypted_signature = ''.join(chr(pow(char, d, n)) for char in signature)
    return decrypted_signature == document
```

### 6. Main Execution
Transactions are signed using RSA, blocks are mined, and the blockchain's integrity is validated.

```python
if __name__ == "__main__":
    participants = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]

    keys = {participant: RSA(61, 53).generate_keys() for participant in participants}  # Пример малых простых чисел

    print("Public Keys of Participants:")
    for participant, (public_key, _) in keys.items():
        print(f" {participant}: {public_key}")
    print()

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

    signed_transactions_1 = []
    for tx in transactions_1:
        sender, _, _ = tx.partition("->")
        _, private_key = keys[sender]
        signature = sign(private_key, tx)
        signed_transactions_1.append(f"{tx}:{signature}")


    blockchain.add_block(signed_transactions_1)

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
- Displays details of each block, including hashes, signed transactions, Merkle roots, and other metadata.
- Indicates whether the blockchain is valid and verifies the integrity of the RSA signatures.

---

## Customization
- Adjust mining difficulty by modifying the `difficulty` parameter in the `Blockchain` constructor.
- Add or modify transactions with appropriate RSA key pairs to test blockchain functionality.
- Generate new RSA key pairs for participants to sign and verify transactions securely.

