from blockchain_api import app
from blockchain_api.blockchain import Blockchain
from flask import jsonify, request
from uuid import uuid4

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():

    # Run PoW algorithm to find next proof
    last_block = blockchain.pop_block
    last_proof = last_block['proof']
    proof = blockchain.hashcash(last_proof)

    # Receive reward for finding proof (sender=0)
    blockchain.new_transaction(
        sender='0',
        recipient=node_id,
        amount=1
    )

    # Forge new block and add it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'new block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    list_values = request.get_json()

    # Validate minimum fields required
    minimum_values = ['sender', 'recipient', 'amount']
    if not all(k in list_values for k in minimum_values):
        return jsonify({'error': 'missing values.'}), 400

    # Create new transaction
    index = blockchain.new_transaction(list_values['sender'], list_values['recipient'], list_values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def entire_chain():

    # Returns current state of the chain
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify({response}), 200

