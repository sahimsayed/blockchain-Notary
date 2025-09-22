import hashlib
import json
from time import time

class Block:
    def __init__(self, document_hash, timestamp=None, previous_hash=None):
        self.document_hash = document_hash
        self.timestamp = timestamp or time()
        self.previous_hash = previous_hash or "0"
        self.block_hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'document_hash': self.document_hash,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("Genesis Block")
        self.chain.append(genesis_block)

    def add_block(self, document_hash):
        last_block = self.chain[-1]
        new_block = Block(document_hash, previous_hash=last_block.block_hash)
        self.chain.append(new_block)

    def verify_document(self, document_hash):
        for block in self.chain:
            if block.document_hash == document_hash:
                return True, self.chain.index(block)
        return False, -1
