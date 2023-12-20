# Spend Funds from Multisig Address
from bitcoin import *
from bitcoin.wallet import CBitcoinSecret, P2SHBitcoinAddress, CBitcoinAddress
from bitcoin.core.script import CScript, OP_2, OP_CHECKMULTISIG
from bitcoin.core import b2x, b2lx, CTransaction, CTxIn, CTxOut, COutPoint
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from Create_2_of_2_Multisig_Script import private_key1, private_key2, redeem_script, address

# Function to create a transaction input (UTXO)
def create_txin(txid, output_index):
    return {'txid': txid, 'vout': output_index}

# Function to create a transaction output
def create_txout(amount, destination_address):
    return {destination_address: amount}

# Function to create and sign a multisig transaction
def create_signed_transaction(inputs, outputs, private_keys, redeem_script):
    tx = CTransaction()
    for i in inputs:
        tx.vin.append(CTxIn(COutPoint(b2lx(i['txid']), i['vout'])))
    
    for addr, amount in outputs.items():
        script_pubkey = CBitcoinAddress(addr).to_scriptPubKey()
        tx.vout.append(CTxOut(amount, script_pubkey))

    for i in range(len(inputs)):
        # Sign the input using private keys and redeem script
        script_sig = CScript([OP_2, *map(lambda key: key.sign(b2lx(inputs[i]['txid']) + bytes([i]), redeem_script), private_keys), redeem_script])
        tx.vin[i].scriptSig = script_sig
        # Verify the script
        VerifyScript(script_sig, tx.vin[i].scriptWitness, tx, i, (SCRIPT_VERIFY_P2SH,))

    return tx

# Function to broadcast the transaction
def broadcast_tx(tx):
    txid = b2lx(tx.GetTxid())
    print("Transaction ID:", txid)
    
# Private keys and multisig address from the previous step
private_key1 = CBitcoinSecret.from_secret_bytes(private_key1)
private_key2 = CBitcoinSecret.from_secret_bytes(private_key2)
address = P2SHBitcoinAddress.from_redeemScript(redeem_script)

# UTXO information
txid = 'transaction_id_of_UTXO'
output_index = 0  # Index of the output in the transaction

# Destination information
destination_address = 'recipient_address'
amount_to_send = 50000  # Amount to send in satoshis

# Create a transaction input (UTXO)
txin = create_txin(txid, output_index)

# Create a transaction output to the desired destination
txout = create_txout(amount_to_send, destination_address)

# Create the transaction
tx = create_signed_transaction([txin], txout, [private_key1, private_key2], redeem_script)

# Broadcast the transaction
broadcast_tx(tx)