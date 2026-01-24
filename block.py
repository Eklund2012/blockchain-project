import hashlib
import time
import json

DIFFICULTY = 4

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
    
    def mine_block(self, difficulty):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
    
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

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
        new_block.mine_block(DIFFICULTY)
        self.chain.append(new_block)

    def create_transaction(self, sender, receiver, amount):
        if not sender or not receiver:
            raise ValueError("Sender and receiver are required")
        
        if amount <= 0: 
            raise ValueError("Amount must be positive")
        
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        block = Block(
            index=len(self.chain),
            data=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )

        block.mine_block(DIFFICULTY)
        self.chain.append(block)

        self.pending_transactions = []


    def is_chain_valid(self):
        target = "0" * DIFFICULTY

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Recalculate has and compare
            if current.hash != current.calculate_hash():
                return False
            
            if not current.hash.startswith(target):
                return False
            
            # Check Chain linkage
            if current.previous_hash != previous.hash:
                return False
            
            for tx in current.data:
                if tx["amount"] <= 0:
                    return False
                
        return True
    
    def save_to_file(self, filename="blockchain.json"):
        with open(filename, "w") as f:
            json.dump(self.chain, f, default=lambda o: o.__dict__, indent=2)

    def load_from_file(self, filename="blockchain.json"):
        with open(filename, "r") as f:
            chain_data = json.load(f)

        self.chain = []
        for block_data in chain_data:
            block = Block(
                block_data["index"],
                block_data["data"],
                block_data["previous_hash"]
            )
            block.timestamp = block_data["timestamp"]
            block.nonce = block_data["nonce"]
            block.hash = block_data["hash"]
            self.chain.append(block)

my_chain = Blockchain()

my_chain.create_transaction("Alice", "Bob", 50)
my_chain.create_transaction("Bob", "Charlie", 25)

my_chain.mine_pending_transactions()

for block in my_chain.chain:
    print("Index:", block.index)
    print("Transactions:", block.data)
    print("Hash:", block.hash)
    print("-" * 30)

print("Is chain valid?", my_chain.is_chain_valid())

my_chain.save_to_file()

new_chain = Blockchain()
new_chain.load_from_file()

print("Loaded chain valid?: ", new_chain.is_chain_valid())

print(type(my_chain.chain[1].data[0]))
