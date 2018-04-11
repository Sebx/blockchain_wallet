import os
from uuid import uuid4
from flask import Flask, json, jsonify, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from blockchain import Blockchain
from transaction_manager import TransactionManager
from models.user import User

# Instantiate the Node
app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# Create dummy users with ids 1 to 5       
users = [User(id, node_identifier) for id in range(1, 6)]

# Instantiate the transaction manager
transaction_manager = TransactionManager(users)

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json(force=True)

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount', 'sender_account', 'destination_account']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    # Apply trasaction on user account
    transaction_manager.apply_transaction(index, values['amount'], values['sender_account'], values['destination_account'])

    response = {'message': "Transaction will be added to Block {0}".format(index)}
    return jsonify(response), 201

@app.route('/transactions', methods=['GET'])
def list_transactions():
    response = {
        'transactions': transaction_manager.report_transactions()
    }
    return jsonify(response), 200

@app.route('/accounts', methods=['GET'])
def list_accounts():
    response = {
        'accounts': transaction_manager.report_accounts()
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
@login_required
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json(force=True)

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

@app.route('/login' , methods=['POST'])
def login():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']

    user = next(iter([user for user in users if user.name == username]), None) 

    if user != None and user.password == password:
        print('Logged in user %s' % (user.name))
        login_user(user)
        return 'Success', 200
    else:
       return 'Error: incorrect credentials', 401

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return 'Error: incorrect credentials', 401

# callback to reload the user object        
@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token != None:
        username, password = token.split(":") # naive token
        user = next(iter([user for user in users if user.name == username]), None)
        if (user != None and user.password == password):
            return user
    return None

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(debug=True, host='0.0.0.0', port=port)
