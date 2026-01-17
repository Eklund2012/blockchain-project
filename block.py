import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        text = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(text.encode()).hexdigest()
    
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            index = len(self.chain),
            data = data,
            previous_hash = latest_block.hash
        )
        self.chain.append(new_block)

my_chain = Blockchain()

my_chain.add_block("First block after genesis")
my_chain.add_block("Second block after genesis")

for block in my_chain.chain:
    print("Index:", block.index)
    print("Data:", block.data)
    print("Hash:", block.hash)
    print("Previous hash:", block.previous_hash)
    print("-" * 30)

my_chain.chain[1].data = "I hacked this block"

for block in my_chain.chain:
    print("Index:", block.index)
    print("Data:", block.data)
    print("Hash:", block.hash)
    print("Previous hash:", block.previous_hash)
    print("-" * 30)