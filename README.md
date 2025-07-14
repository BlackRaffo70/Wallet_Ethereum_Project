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

## 📁 Esempio di struttura del progetto

Eth_walletSIM 2/
│
├── wallet_main.py

├── wallet_contract.sol

├── wallet_contract.json

├── wallet.json

├── .env

└── venv/

## 🧪 Requisiti

- Python 3.8.6+
- Ganache ( Impostando limite gas a 12000000 (12M)
- Moduli: `web3`, `python-dotenv`, `py-solc-x`

## ▶️ Esecuzione

1. Configurazione  file `.env` con:
- WEB3_PROVIDER_URL=http://127.0.0.1:7545
- CHIAVE_PRIVATA_1=...
- CHIAVE_PRIVATA_2=...

2. Avvia Ganache.

3. Esegui:
#!/bin/bash

- python3 -m venv venv

- source venv/bin/activate

- pip install --upgrade pip

- pip install web3 python-dotenv py-solc-x

- python wallet_main.py

Ho creato un ambiente virtuale (venv) per: 
- Isolare le dipendenze del progetto da quelle di sistema
- Evitare conflitti tra versioni di librerie in progetti diversi
- Rendere il progetto portabile, facilitando la riproducibilità su altri ambienti o macchine

 
 ## 🖥️ Output attesi
Eseguendo lo script wallet_main.py, si ottiene una sequenza di messaggi nel terminale che confermano le varie fasi del processo:

<img width="1406" height="314" alt="Screenshot 2025-07-11 alle 15 54 31" src="https://github.com/user-attachments/assets/923103d2-855a-4d9e-b77d-69c0da559b92" />


Questi messaggi indicano:
Lettura corretta dell’ambiente e connessione al nodo Ethereum
Compilazione del contratto Solidity (.sol)
Deploy del wallet sulla blockchain (con indirizzo generato)
Invio di ETH da un account all’altro e successivo submit della transazione

<img width="1201" height="380" alt="image" src="https://github.com/user-attachments/assets/531c4389-0f0d-444d-9f40-df697eec75bf" />

📸 Esempio da Ganache
Nella schermata inclusa, Ganache mostra:

Un primo account ha inviato una transazione da 0.1 ETH a un secondo account.
Il mittente ha pagato 0.1 ETH + costo del gas (quindi ha perso leggermente più di 0.1).
Il destinatario ha ricevuto esattamente 0.1 ETH, perché il costo del gas viene pagato solo dal mittente.
Ogni transazione è stata automaticamente minata nel proprio blocco grazie all'opzione AUTOMINING.

<img width="1201" height="405" alt="image" src="https://github.com/user-attachments/assets/46783571-9187-4298-93c7-4276727c5872" />


-  **🧱 Blocco 0 (Genesis)** – Blocco iniziale creato automaticamente da Ganache, senza transazioni.
-  **🚀 Blocco 1** – Deploy del contratto MultiSigWallet (gas alto: 8.000.000).
-  **💸 Blocco 2** – Invio di 0.1 ETH dal primo al secondo account (gas minimo: 21.000).
-  **✍️ Blocco 3** – Chiamata a `submitTransaction` per proporre una transazione.



<img width="1201" height="573" alt="image" src="https://github.com/user-attachments/assets/4b7b523f-09af-4cd8-a910-a3b6988f2bd8" />



Questa schermata di Ganache mostra le 3 transazioni eseguite durante il test:

-  **🔧 Contract Creation** – Deploy del contratto MultiSigWallet, con alto consumo di gas (8.000.000), ma nessun trasferimento di ETH.
-  **💸 Value Transfer** – Invio di 0.1 ETH (in wei) dal primo al secondo account.
-  **📞 Contract Call** – Chiamata a `submitTransaction()` per proporre una transazione.





