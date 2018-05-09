from time import time
import hashlib
import json


def new_transaction(block_chain, sender, recipient, amount):
    """
    Adds a new transaction to the list of transactions
    在列表中添加新交易后，返回该交易被加到的区块的索引，也就是下一个要挖的区块
    :param block_chain
    :param sender:<str> Address of the Sender
    :param recipient:<str> Address of the recipient
    :param amount:<int> Amount
    :return:<int> The index of the Block that will hold the transaction
    """
    transaction = {
        'ver': 1,
        'time': time(),
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    transaction['hash'] = tx_hash(transaction)
    block_chain.current_transactions.append(transaction)
    return block_chain.last_block['index'] + 1


def tx_hash(tx):
    """
    Creates a SHA-256 hash of a transaction
    :param tx:<dict> Transaction
    :return:<str> Hash result
    """
    tx_str = json.dumps(tx, sort_keys=True).encode()
    return hashlib.sha256(tx_str).hexdigest()


def get_txs_merkle_root(txs):
    """
    组件交易记录的merkle树，并返回根Hash
    :param txs:
    :return:
    """
    txs_hash = [tx["hash"] for tx in txs]
    tmp_txs = []
    while len(txs_hash) >= 2:
        index = 0
        while index < len(txs_hash):
            hash1 = txs_hash[index]
            index += 1
            if index >= len(txs_hash):
                hash2 = ""
            else:
                hash2 = txs_hash[index]
            index += 1
            p_hash = hashlib.sha256(bytes.fromhex(hash1 + hash2)).hexdigest()
            tmp_txs.append(p_hash)
        txs_hash = tmp_txs[:]
        tmp_txs = []
    if txs_hash:
        return txs_hash[0]
    else:
        return ""
