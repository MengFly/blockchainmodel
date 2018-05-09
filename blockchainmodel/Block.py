from blockchainmodel.util import constant
from blockchainmodel.util import hash
from blockchainmodel import Tx


def new_block(block_chain, txs, proof, timestamp, previous_hash=None):
    merkle_root = Tx.get_txs_merkle_root(txs=txs)
    block_chain.transactions += txs
    # get txs the hash columns, make a list as block params
    txs_hash = [tx["hash"] for tx in txs]

    block = {
        'version': constant.VERSION,
        'previous_hash': previous_hash or block_chain.chain[-1]["hash"],
        'merkle_root': merkle_root,
        'index': len(block_chain.chain) + 1,
        'timestamp': timestamp,
        'tx_n': len(txs_hash),
        'tx': txs_hash,
        'difficulty_target': constant.DIFFICULTY_BITS,
        'proof': proof
    }
    # block_hash = hash.hash_block(block)
    # block["hash"] = block_hash
    # Reset the current list of transactions
    block_chain.current_transactions = []
    block_chain.chain.append(block)
    return block


def block_head_hash(block):
    """
    挖矿算法：SHA256(SHA256(version + prev_hash + ntime + nbits + x )) < TARGET
    Creates a SHA-256 hash of a Block
    :param block:<dict> Block
    :return:<str> Hash result
    """
    # We must make sure the Dictionary is Ordered, or we'll have inconsistent hashes
    ver = block["version"]
    pre_hash = block["previous_hash"]
    merkle_root = block["merkle_root"]
    proof = hash.hash_proof(block["proof"])
    print(ver + pre_hash + merkle_root)
    return hash.hash2(ver + pre_hash + merkle_root + proof)
