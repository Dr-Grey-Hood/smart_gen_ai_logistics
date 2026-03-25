# models/blockchain.py
"""
Simple blockchain for logging events (predictions, feedback, transactions).
just an append-only chain with proof-of-work
suitable for auditability and tamper-evidence.
"""

import hashlib
import json
import time
from typing import List, Dict, Any
from pathlib import Path

CHAIN_FILE = Path("blockchain_data.json")  # file to persist the chain

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict[str, Any]], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }

class SimpleBlockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty  # number of leading zeros required in hash
        self.chain: List[Block] = []
        self.current_transactions: List[Dict[str, Any]] = []
        # load chain from disk if exists
        if CHAIN_FILE.exists():
            self._load_chain()
        else:
            # Create genesis block
            genesis = Block(index=0, timestamp=time.time(), transactions=[{"genesis": True}], previous_hash="0", nonce=0)
            genesis.nonce, _ = self.proof_of_work(genesis)
            self.chain = [genesis]
            self._save_chain()

    # ---------- transaction management ----------
    def new_transaction(self, tx: Dict[str, Any]) -> int:
        """
        Add a new transaction to the list of current transactions.
        Returns the index of the block that will hold this transaction (next block).
        """
        self.current_transactions.append(tx)
        return self.last_block().index + 1

    # ---------- block creation ----------
    def last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> (int, str):
        """
        Simple proof-of-work: find a nonce so that hash(block_dict + nonce) has leading zeros.
        Returns (nonce, hash).
        """
        block.nonce = 0
        computed_hash = self.hash_block(block)
        target = "0" * self.difficulty
        while not computed_hash.startswith(target):
            block.nonce += 1
            computed_hash = self.hash_block(block)
        return block.nonce, computed_hash

    def hash_block(self, block: Block) -> str:
        """
        Create a SHA-256 hash of a block (consistent serialization).
        """
        block_string = json.dumps(block.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, nonce: int, previous_hash: str = None) -> Block:
        """
        Create a new Block with the current transactions and append to the chain.
        Clears current_transactions.
        """
        prev_hash = previous_hash or self.hash_block(self.last_block())
        block = Block(
            index = self.last_block().index + 1,
            timestamp = time.time(),
            transactions = self.current_transactions.copy(),
            previous_hash = prev_hash,
            nonce = nonce
        )
        self.current_transactions = []
        self.chain.append(block)
        self._save_chain()
        return block

    # ---------- validation ----------
    def is_valid_chain(self, chain: List[Dict[str, Any]] = None) -> bool:
        """
        Validate chain (list of dicts) or current chain.
        """
        if chain is None:
            chain = [b.to_dict() for b in self.chain]

        for i in range(1, len(chain)):
            prev = chain[i-1]
            curr = chain[i]
            # Recreate block objects to compute hashes
            prev_block = Block(prev['index'], prev['timestamp'], prev['transactions'], prev['previous_hash'], prev['nonce'])
            curr_block = Block(curr['index'], curr['timestamp'], curr['transactions'], curr['previous_hash'], curr['nonce'])

            # Check previous_hash link
            if curr['previous_hash'] != self.hash_block(prev_block):
                return False

            # Check proof-of-work
            if not self.hash_block(curr_block).startswith("0" * self.difficulty):
                return False

        return True

    # ---------- persistence ----------
    def _save_chain(self):
        data = [b.to_dict() for b in self.chain]
        CHAIN_FILE.write_text(json.dumps(data, indent=2))

    def _load_chain(self):
        raw = CHAIN_FILE.read_text()
        data = json.loads(raw)
        self.chain = [Block(d['index'], d['timestamp'], d['transactions'], d['previous_hash'], d.get('nonce', 0)) for d in data]

    # ---------- helper views ----------
    def get_chain(self) -> List[Dict[str, Any]]:
        return [b.to_dict() for b in self.chain]

    def get_pending_transactions(self) -> List[Dict[str, Any]]:
        return self.current_transactions.copy()

# Singleton instance (easier to import)
blockchain = SimpleBlockchain(difficulty=3)
