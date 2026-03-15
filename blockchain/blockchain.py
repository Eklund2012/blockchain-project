import json
from blockchain.block import Block

DIFFICULTY = 4

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
            index=len(self.chain),
            data=data,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def save_to_file(self, filename="blockchain.json"):
        with open(filename, "w") as f:
            json.dump([{
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            } for block in self.chain], f, indent=2)

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
            block.hash = block_data["hash"]
            self.chain.append(block)

def example_run():
    my_chain = Blockchain()
    my_chain.add_block({"action": "Fix bug #123", "details": "Changed function X"})
    my_chain.add_block({"action": "Write report", "details": "Version 1.0"})

    for block in my_chain.chain:
        print(f"Index: {block.index}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print("-" * 40)

    print("Chain valid?", my_chain.is_chain_valid())

    # Spara och läs tillbaka
    my_chain.save_to_file()
    new_chain = Blockchain()
    new_chain.load_from_file()
    print("Loaded chain valid?", new_chain.is_chain_valid())

def hacked_example_run():
    new_chain = Blockchain()
    new_chain.load_from_file()
    print("Loaded chain valid?", new_chain.is_chain_valid())

# Exempel på användning
if __name__ == "__main__":
    example_run()

    hacked_example_run()
