from time import time
from urllib.parse import urlparse
import requests
from blockchainmodel import MineModel
from blockchainmodel import Block


class Blockchain(object):
    """
    负责管理链。
    用来存储交易信息
    一些帮助方法来将新区块添加到链中
    """

    def __init__(self):
        # Save the Blockchain
        self.chain = []
        # Save the current transactions
        self.current_transactions = []
        self.transactions = []
        self.nodes = set()

        # Create the genesis block(创建创世区块）
        Block.new_block(
            block_chain=self,
            txs=self.current_transactions,
            previous_hash="0000000000000000000000000000000000000000000000000000000000000000",
            proof=100,
            timestamp=str(time()).split(".")[0])

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address:<str> Address of node.Eg. 'Http://192.168.0.5:5000'
        :return:None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url)


    def valid_chain(self, chain):
        """
        检查链的有效性，便利每个区块，验证哈希和工作量证明
        Determine if given a blockchain is valid
        :param chain:<list> A blockchain
        :return:<bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n--------------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != Block.block_head_hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not MineModel.valid_proof(block["version"], block["timestamp"], block["previous_hash"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        遍历所有的邻居节点，下载它们的链。用valid_chain放发进行验证，
        如果找到了有效链，而且长度比本地的要长，就替换掉本地的链
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network
        :return:<bool> True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

            if new_chain:
                self.chain = new_chain
                return True
            return False
