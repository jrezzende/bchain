# -*- coding: utf-8 -*-

from time import time
from urllib.parse import urlparse
import requests
import hashlib
import json


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set()

    @property
    def pop_block(self):
        return self.chain[-1]

    def register_node(self, url):
        parsed_url = urlparse(url)
        self.nodes.add(parsed_url.netloc)

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

        while self.proof_of_work(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def proof_of_work(last_proof, proof):

        attempt = f'{last_proof}{proof}'.encode()
        attempt_hash = hashlib.sha256(attempt).hexdigest()

        return attempt_hash[:3] == '000'

    def valid_chain(self, chain):

        last_block = chain[0]
        index = 1

        while index < len(chain):
            block = chain[index]

            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.proof_of_work(last_block['proof'], block['proof']):
                return False

            last_block = block
            index += 1

        return True

    def consensus(self):

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
