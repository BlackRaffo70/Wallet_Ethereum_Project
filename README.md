# 🔐 Eth_walletSIM – Simulatore di Wallet Multi-Sig su Ethereum

La mia prova pratica è consistita in una **simulazione di un wallet Multi-Signature** su blockchain Ethereum, realizzata per la prova di Sicurezza dell’Informazione.

## 📦 Contenuto del progetto

- `wallet_contract.sol` – Contratto Solidity che implementa un wallet multi-firma.
- `wallet_main.py` – Script Python che compila, deploya e interagisce con il contratto.
- `wallet_contract.json` – ABI e bytecode generati dalla compilazione.
- `.env` – File con variabili d’ambiente (URL RPC, chiavi private).

## ⚙️ Funzionalità implementate

### ✅ Setup

- Connessione a un nodo Ganache.
- Lettura delle chiavi private e configurazione degli account.
- Verifica del gas limit e connessione alla chain.

### 🛠️ Compilazione del contratto

- Utilizza Solidity 0.8.26.
- Estrae ABI e bytecode.
- Salva l'output in formato JSON.

### 🚀 Deploy del contratto

- Deploy del wallet MultiSig con 2 proprietari.
- 1 conferma richiesta per eseguire una transazione.
- Stampa dell’indirizzo del contratto.

### 💸 Invio di ETH diretto

- Trasferimento diretto di **0.01 ETH** da `owners[0]` a `owners[1]`.

### 📝 Proposta di transazione MultiSig

- Due chiamate a `submitTransaction` sul contratto per proporre una transazione da 0.002 ETH.

## ⚠️ Funzionalità **non** ancora implementate

- `confirmTransaction` – conferma delle transazioni proposte.
- `executeTransaction` – esecuzione delle transazioni confermate.
- Verifica della sicurezza e test automatici.

## 📁 Esempio di struttura del progetto

Eth_walletSIM 2/
│
├── wallet_main.py
│
├── wallet_contract.sol
│
├── wallet_contract.json
│
├── wallet.json
│
├── .env
│
└── venv/

## 🧪 Requisiti

- Python 3.9+
- Ganache
- Moduli: `web3`, `python-dotenv`, `py-solc-x`

## ▶️ Esecuzione

1. Configura il file `.env` con:
WEB3_PROVIDER_URL=http://127.0.0.1:7545
CHIAVE_PRIVATA_1=...
CHIAVE_PRIVATA_2=...

2. Avvia Ganache.

3. Esegui:
#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install web3 python-dotenv py-solc-x

python wallet_main.py

Abbiamo creato un ambiente virtuale (venv) per: 
-Isolare le dipendenze del progetto da quelle di sistema
-Evitare conflitti tra versioni di librerie in progetti diversi
-Rendere il progetto portabile, facilitando la riproducibilità su altri ambienti o macchine

