from blockchain_api import app
from blockchain_api.blockchain import Blockchain
from flask import jsonify, request
from uuid import uuid4

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/nodes/register', methods=['POST'])
def register_nodes():

    list_values = request.get_json()
    nodes = list_values.get('nodes')

    if nodes is None:
        return jsonify({'error': 'must supply a list of nodes to be registered.'}), 400

    for node in nodes:
        blockchain.register_node(node)

    return jsonify({'message': 'nodes have been added', 'nodes': list(blockchain.nodes)}), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus_alg():

    replaced = blockchain.consensus()

    if replaced:
        response = {
            'message': 'chain replaced',
            'new_chain': blockchain.chain
        }

    else:
        response = {
            'message': 'current chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


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

    return jsonify(response), 200

