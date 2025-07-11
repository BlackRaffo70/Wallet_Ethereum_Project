"""
Multi-sig wallet demo:
• compila il contratto Solidity
• lo distribuisce su Ganache
• esegue un test completo: deposito, proposta, conferma, esecuzione
"""

import os, json, time
from dotenv import load_dotenv
from web3 import Web3
from solcx import install_solc, set_solc_version, compile_standard

# ------------------------------------------------------------------
# 1 Configurazione ambiente
# ------------------------------------------------------------------
load_dotenv()                                     # legge variabili da .env

RPC_URL = os.getenv("WEB3_PROVIDER_URL")          # es. http://127.0.0.1:7545
PRIVATE_KEYS = [                                  # due owner del wallet
    os.getenv("CHIAVE_PRIVATA_1"),
    os.getenv("CHIAVE_PRIVATA_2"),
]

if not RPC_URL or not all(PRIVATE_KEYS):
    raise SystemExit("⚠️  .env incompleto – verifica URL e chiavi private")

# ------------------------------------------------------------------
# 2 Connessione a Ganache
# ------------------------------------------------------------------
w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise SystemExit("⚠️  impossibile connettersi a Ganache")

block_gas_limit = w3.eth.get_block("latest").gasLimit

owners = [w3.eth.account.from_key(pk) for pk in PRIVATE_KEYS]
owner_addresses = [acc.address for acc in owners]

print("🌐 chain ID:", w3.eth.chain_id)
for i, acc in enumerate(owners, 1):
    balance = w3.from_wei(w3.eth.get_balance(acc.address), "ether")
    print(f"  owner {i}: {acc.address} – {balance} ETH")

# ------------------------------------------------------------------
# 3 Compilazione contratto
# ------------------------------------------------------------------
def compile_contract(path="MultiSigWallet.sol", name="MultiSigWallet"):
    install_solc("0.8.26")
    set_solc_version("0.8.26")

    source = open(path).read()
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {path: {"content": source}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
        },
        solc_version="0.8.26",
    )

    abi  = compiled["contracts"][path][name]["abi"]
    code = compiled["contracts"][path][name]["evm"]["bytecode"]["object"]

    json.dump({"abi": abi, "bytecode": code}, open(f"{name}.json", "w"), indent=2)
    print("🛠️  compilazione completata")
    return abi, code

# ------------------------------------------------------------------
# 4 Helper generico per inviare transazioni
# ------------------------------------------------------------------
def send_tx(callable_tx, signer, gas=block_gas_limit - 5000):
    tx = callable_tx.build_transaction(
        {
            "from":   signer.address,
            "nonce":  w3.eth.get_transaction_count(signer.address),
            "gas":    gas,
            "gasPrice": w3.eth.gas_price,
            "chainId":  w3.eth.chain_id,
        }
    )
    signed = w3.eth.account.sign_transaction(tx, signer.key)
    hash_  = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(hash_)
    return receipt

# ------------------------------------------------------------------
# 5 Deploy del wallet
# ------------------------------------------------------------------
def deploy_wallet(abi, bytecode, owners, confirmations, deployer):
    factory = w3.eth.contract(abi=abi, bytecode=bytecode)
    receipt = send_tx(
        factory.constructor(owners, confirmations),
        deployer
    )
    print("🚀 contratto creato @", receipt.contractAddress)
    return receipt.contractAddress

# ------------------------------------------------------------------
# 6 Funzioni di utilità
# ------------------------------------------------------------------
def show_balance(addr, label="saldo"):
    bal = w3.from_wei(w3.eth.get_balance(addr), "ether")
    print(f"{label}: {bal} ETH")

# ------------------------------------------------------------------
# 7 Flusso principale
# ------------------------------------------------------------------
if __name__ == "__main__":
    abi, bytecode = compile_contract()

    wallet_addr = deploy_wallet(
        abi, bytecode, owner_addresses, confirmations=1, deployer=owners[0]
    )
    wallet = w3.eth.contract(address=wallet_addr, abi=abi)

    # deposito di 0.01 ETH nel wallet
    tx_hash = w3.eth.send_transaction(
        {
            "from": owners[0].address,
            "to":   wallet_addr,
            "value": w3.to_wei(0.01, "ether"),
            "gas":  210_000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(owners[0].address),
            "chainId": w3.eth.chain_id,
        }
    )
    w3.eth.wait_for_transaction_receipt(tx_hash)
    show_balance(wallet_addr, "📥 dopo deposito")

    # proposta di pagamento 0.002 ETH a un indirizzo di test
    recipient = "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"
    submit_receipt = send_tx(
        wallet.functions.submitTransaction(recipient, w3.to_wei(0.002, "ether"), b""),
        owners[0]
    )
    tx_index = wallet.events.SubmitTransaction().process_receipt(submit_receipt)[0].args.txIndex
    print("📝 proposta registrata – index", tx_index)

    # conferma ed esecuzione
    send_tx(wallet.functions.confirmTransaction(tx_index), owners[1])
    send_tx(wallet.functions.executeTransaction(tx_index), owners[0])

    # saldo finale
    show_balance(wallet_addr, "📤 dopo esecuzione")
