from flask import Flask, jsonify, render_template
from blockchainmodel.util.param_check import param_check, get_params
import blockchainmodel.util.constant as constant
from blockchainmodel import MineModel
from time import time
from blockchainmodel import Tx
from blockchainmodel import Block
from blockchainmodel.Blockchain import Blockchain

app = Flask(__name__)

# 初始化Blockchain类
blockchain = Blockchain()


# 获取全部区块链信息
@app.route('/chain', methods=["GET"])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# 获取未被打包的交易列表
@app.route('/tx/not_sure', methods=["GET"])
def get_not_sure_tx():
    response = {
        'tx': blockchain.current_transactions,
        'length': len(blockchain.current_transactions)
    }
    return jsonify(response), 200


# 用户交易实现
@app.route("/tx/new", methods=["POST"])
def new_transactions():
    param_list = ['sender', 'recipient', 'amount']
    params = get_params(param_list)

    # Check that the required field are in the POST'ed data
    is_check, error_param_index = param_check(params)
    if is_check:
        return "Miss Param " + param_list[error_param_index], 400
    # Create a new Transaction
    new_transaction_index = Tx.new_transaction(block_chain=blockchain, sender=params[0],
                                               recipient=params[1], amount=params[2])
    response = {"message": f'Transaction will be added to Block {new_transaction_index}'}
    return jsonify(response), 201


@app.route("/")
def index():
    return render_template('/index.html')


# 挖矿段的实现
"""
1.计算工作量证明
2.奖励矿工，新增一次交易就赚一个币
3.将区块加入链就可以新建区块
"""


@app.route("/mine", methods=["POST"])
def mine():
    # get mine address, if mine success, this address will get some coins
    mine_address = get_params(['address'])[0]
    # check address
    if param_check([mine_address])[0]:
        return "Miss Mine Address", 400

    last_block = blockchain.last_block
    previous_hash = Block.block_head_hash(last_block)
    # We must receive a reward for finding the proof
    # The sender is "0" to signify that this node has mined a new coin

    Tx.new_transaction(
        block_chain=blockchain,
        sender=0,
        recipient=mine_address,
        amount=1
    )
    # We run the proof work algorithm to get the next proof...
    proof = MineModel.proof_of_work(constant.VERSION, blockchain.current_transactions, previous_hash)

    block = Block.new_block(
        block_chain=blockchain,
        txs=blockchain.current_transactions,
        proof=proof,
        timestamp=time(),
        previous_hash=previous_hash)
    response = {
        "message": "New Block Forged",
        "index": block['index'],
        'tx': block['tx'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=["POST"])
def register_nodes():
    address = get_params(['address'])[0]

    if param_check([address])[0]:
        return "Error: Please enter address", 400
    # register neighbours address
    blockchain.register_node(address)
    response = {
        'message': "New nodes have been added",
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/get_register', methods=["GET"])
def get_register():
    response = {
        'total_nodes': list(blockchain.nodes),
        'length': len(blockchain.nodes)
    }
    return jsonify(response), 200


@app.route("/nodes/resolve", methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': "Our chain is replaced",
            'chain': blockchain.chain
        }
    else:
        response = {
            'message': "Out chain is authoritative",
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run("127.0.0.1", port=5002)
