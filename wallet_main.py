
#!/usr/bin/env python3

import os, json, re
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import Web3RPCError
from solcx import (
    install_solc, set_solc_version, compile_standard,
    get_installed_solc_versions,
)

# ---------- 1. ambiente ----------
load_dotenv()
RPC_URL = os.getenv("WEB3_PROVIDER_URL")
PRIVATE_KEYS = [os.getenv("CHIAVE_PRIVATA_1"), os.getenv("CHIAVE_PRIVATA_2")]
if not RPC_URL or not all(PRIVATE_KEYS):
    raise SystemExit(".env incompleto (URL o chiavi mancanti)")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    raise SystemExit("Nodo Ganache non raggiungibile")

owners       = [w3.eth.account.from_key(k) for k in PRIVATE_KEYS]
owner_addrs  = [o.address for o in owners]
print("⛽ block gas limit:", w3.eth.get_block("latest").gasLimit)

# ---------- 2. compilazione ----------
def compile_contract(src="wallet_contract.sol", name="wallet_contract"):
    if "0.8.17" not in get_installed_solc_versions():
        install_solc("0.8.17")
    set_solc_version("0.8.17")

    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {src: {"content": open(src).read()}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
        },
        solc_version="0.8.17",
    )
    abi  = compiled["contracts"][src][name]["abi"]
    byte = compiled["contracts"][src][name]["evm"]["bytecode"]["object"]
    json.dump({"abi": abi, "bytecode": byte}, open(f"{name}.json", "w"), indent=2)
    print("🛠️  contratto compilato")
    return abi, byte

# ---------- 3. tx helper ----------
TX_HASH_RE = re.compile(r"0x[a-fA-F0-9]{64}")

def send_tx(callable_tx, signer, gas=8_000_000):
    tx = callable_tx.build_transaction({
        "from":   signer.address,
        "nonce":  w3.eth.get_transaction_count(signer.address),
        "gas":    gas,
        "gasPrice": w3.eth.gas_price,
        "chainId":  w3.eth.chain_id,
    })
    signed = w3.eth.account.sign_transaction(tx, signer.key)
    try:
        h = w3.eth.send_raw_transaction(signed.raw_transaction)
        return w3.eth.wait_for_transaction_receipt(h)
    except Exception as e:
        raise RuntimeError(f"❌ Deploy fallito: {e}")


# ---------- 4. deploy ----------
def deploy_wallet(abi, bytecode, addrs, req, deployer):
    factory = w3.eth.contract(abi=abi, bytecode=bytecode)
    rec = send_tx(factory.constructor(addrs, req), deployer)
    print("🚀 wallet @", rec.contractAddress)
    return rec.contractAddress

# ---------- 5. flow ----------
if __name__ == "__main__":
    with open("truffle/build/contracts/wallet_contract.json") as f:
        contract_data = json.load(f)

    abi = contract_data["abi"]
    wallet_addr = "0x333481e5198ef27c2867Be8d82b7FB8d9CC4cEe0"  # <- indirizzo del contratto truffle

    wallet = w3.eth.contract(address=wallet_addr, abi=abi)

    # Invia 7 ETH al contratto
    tx_hash = w3.eth.send_transaction({
        "from": owners[0].address,  # Uno degli account Ganache
        "to": wallet_addr,  # Indirizzo del contratto
        "value": w3.to_wei(10, "ether"),  # Quanto ETH vuoi inviare
        "gas": 210000,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(owners[0].address),
        "chainId": w3.eth.chain_id,
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)

    print("📬 Wallet finanziato con 5 ETH")

    # --- deposito 1 ETH ---
    tx_hash = w3.eth.send_transaction(
        {
            "from":  owners[0].address,
            "to":    owners[1].address,
            "value": w3.to_wei(1, "ether"),
            "gas":   210_000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(owners[0].address),
            "chainId": w3.eth.chain_id,
        }
    )
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("📥 deposito eseguito")


    # --- submit ---
    recipient = owner_addrs[0]
    rec = send_tx(
        wallet.functions.submitTransaction(
            recipient,
            w3.to_wei(5, "ether"),
            b""  # dati vuoti
        ),
        owners[0]
    )

    tx_index = wallet.functions.getTransactionCount().call() -1
    rec = send_tx(
        wallet.functions.confirmTransaction(tx_index),
        owners[1]
    )

    tx_index = wallet.functions.getTransactionCount().call() -1
    rec = send_tx(
        wallet.functions.executeTransaction(tx_index),
        owners[0]
    )

    print("✅ transazione eseguita")

    print("💰 Saldo wallet:", w3.from_wei(w3.eth.get_balance(wallet_addr), "ether"), "ETH")
