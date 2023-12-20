# Spend Locked Funds
from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

import requests

from Create_P2PKH_Script import private_key, address


def create_txin(txid, output_index):
    return CMutableTxIn(COutPoint(txid, output_index))


def create_txout(amount_to_send, destination_address):
    return CMutableTxOut(amount_to_send, destination_address)


def create_signed_transaction(txin, txout, private_key):
    tx = CMutableTransaction([txin], [txout])

    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(private_key.pub), OP_EQUALVERIFY, OP_CHECKSIG])
    
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    sig = private_key.sign(sighash) + bytes([SIGHASH_ALL])

    txin.scriptSig = CScript([sig, private_key.pub])

    VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

    return tx


def broadcast_tx(tx):
    tx_hex = tx.serialize().hex()
    print('Transaction hex:', tx_hex)



if __name__ == '__main__':
    SelectParams('testnet') 

    # Create a transaction input (UTXO)
    txid = lx('7e195aa3de827814f172c362fcf838d92ba10e3f9fdd9c3ecaf79522b311b22d') # Transaction ID of the UTXO you want to spend
    output_index = 0 # Index of the output in the transaction
    txin = create_txin(txid, output_index)

    # Create a transaction output to the desired destination
    destination_address = address.to_scriptPubKey()
    amount_to_send = 0.001*COIN # Amount to send in satoshis
    txout = create_txout(amount_to_send, destination_address)

    # Create the transaction
    tx = create_signed_transaction(txin, txout, private_key)

    # Broadcast the transaction
    broadcast_tx(tx)