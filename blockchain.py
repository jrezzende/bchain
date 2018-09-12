# -*- coding: utf-8 -*-
from time import time
import hashlib
import json


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    @property
    def pop_block(self):
        return self.chain[-1]

    def new_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.pop_block['index'] + 1

    @staticmethod
    def hash(block):
        sorted_block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(sorted_block_string).hexdigest()

    def hashcash(self, last_proof):

        # basic PoW algorithm:
        # - Find a number p in which a hash(p') containing 3 leading zeroes.
        # - p is the previous proof and p' is the new proof.

        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):

        attempt = f'{last_proof}{proof}'.encode()
        attempt_hash = hashlib.sha256(attempt).hexdigest()
        return attempt_hash[:3] == '000'
