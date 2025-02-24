import hashlib
import time
import json
import datetime

# Defined a class to represent a block in the blockchain
class LedgerEntry:
    def __init__(self, entry_id, previous_identifier, data_records, timestamp=None, iteration_counter=0):
        # Initialize a block with entry ID, previous identifier, data records, timestamp, iteration counter, and hash
        self.entry_id = entry_id
        self.previous_identifier = previous_identifier
        self.data_records = data_records
        self.timestamp = timestamp or time.time()
        self.iteration_counter = iteration_counter
        # Calculate the hash of the block based on its data
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Convert block data into a JSON string and calculate its SHA-256 hash
        block_data = {
            'entry_id': self.entry_id,
            'previous_identifier': self.previous_identifier,
            'data_records': self.data_records,
            'timestamp': self.timestamp,
            'iteration_counter': self.iteration_counter
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_ledger_entry(self, complexity_level):
        # Implement a basic proof-of-work mechanism to make block creation computationally intensive
        target = '0' * complexity_level
        while self.hash[:complexity_level] != target:
            self.iteration_counter += 1
            # Recalculate hash with updated iteration counter
            self.hash = self.calculate_hash()
        print(f"Ledger entry mined: {self.hash}")

# Defined a class to manage the chain of blocks
class DistributedLedger:
    def __init__(self, complexity_level=4):
        # Initialize the blockchain with a genesis block and set complexity level
        self.chain = [self.create_genesis_block()]
        self.complexity_level = complexity_level
        self.pending_data_records = []

    def create_genesis_block(self):
        # Create the genesis block (the first block in the chain)
        return LedgerEntry(0, "0", ["Genesis Block"], time.time())

    def get_latest_block(self):
        # Get the latest block in the chain
        return self.chain[-1]

    def add_data_record(self, data_record):
        # Add a new data record to the list of pending data records
        self.pending_data_records.append(data_record)

    def mine_pending_data_records(self):
        # Mine a new block with the pending data records
        if not self.pending_data_records:
            print("No data records to mine.")
            return

        new_block = LedgerEntry(len(self.chain), self.get_latest_block().hash, self.pending_data_records)
        new_block.mine_ledger_entry(self.complexity_level)
        self.chain.append(new_block)
        self.pending_data_records = []

    def validate_chain_integrity(self):
        # Validate the integrity of the blockchain by checking hashes and previous identifiers
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.entry_id} hash is invalid!")
                return False

            if current_block.previous_identifier != previous_block.hash:
                print(f"Block {current_block.entry_id} previous identifier mismatch!")
                return False

        return True

    def print_chain(self):
        # Print the details of each block in the blockchain
        for block in self.chain:
            readable_time = datetime.datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S') # Convert timestamp to human-readable format
            print(f"Block {block.entry_id} [Hash: {block.hash}, Previous Identifier: {block.previous_identifier}, Data Records: {block.data_records}, Timestamp: {readable_time}, Iteration Counter: {block.iteration_counter}]")

if __name__ == "__main__":
    my_distributed_ledger = DistributedLedger()

    # Get user input for the number of blocks to mine
    num_blocks_to_mine = int(input("Enter the number of blocks to mine: "))

    for i in range(num_blocks_to_mine):
        print(f"\nAdding data records and mining block {i + 1}...")
        my_distributed_ledger.add_data_record(f"Data Record {i + 1}")
        my_distributed_ledger.mine_pending_data_records()

    print("\nBlockchain:")
    my_distributed_ledger.print_chain()

    print("\nIs blockchain valid?", my_distributed_ledger.validate_chain_integrity())

    # Get user input for the block to tamper with
    block_to_tamper = int(input("\nEnter the block index to tamper with (1 to {}): ".format(num_blocks_to_mine)))

    if 1 <= block_to_tamper <= num_blocks_to_mine:
        print(f"\nTampering with block {block_to_tamper}...")
        my_distributed_ledger.chain[block_to_tamper].data_records = ["Tampered Data Record"]
    else:
        print("Invalid block index!")

    print("\nBlockchain after tampering:")
    my_distributed_ledger.print_chain()

    print("\nIs blockchain valid after tampering?", my_distributed_ledger.validate_chain_integrity())
