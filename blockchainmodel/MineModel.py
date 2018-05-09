from blockchainmodel.util import hash
from blockchainmodel.util import constant
from blockchainmodel import Tx


def proof_of_work(version, txs, pre_hash):
    """
    工作量证明机制
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    :param pre_hash:
    :param txs All of not sure tx_hash
    :param version:
    :return:<int>
    """
    proof = 0
    merkle_root = Tx.get_txs_merkle_root(txs)
    while valid_proof(version=version, pre_hash=pre_hash,
                      merkle_root=merkle_root, proof=proof) is False:
        proof += 1
    return proof


def valid_proof(version, pre_hash, merkle_root, proof):
    """
    Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeros?
    :param pre_hash:
    :param version:
    :param proof:<int> Current Proof
    :param merkle_root
    :return:<bool> True if correct, False if not...
    """
    target = 2 ** (256 - constant.DIFFICULTY_BITS)
    guess = version + pre_hash + merkle_root + hash.hash_proof(proof)
    guess_hash = hash.hash2(guess)
    return int(guess_hash, 16) < target
