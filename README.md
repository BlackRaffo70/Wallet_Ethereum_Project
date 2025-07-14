# 🔐 Eth\_walletSIM – Simulatore di Wallet Multi‑Sig su Ethereum

> **Simulazione** di un portafoglio smart‑contract multi‑firma (m‑of‑n) sviluppato per l’esame di **Sicurezza dell’Informazione**. Il progetto mostra tutte le fasi di *compilazione, deploy e uso* di un Multi‑Sig Wallet su una blockchain Ethereum locale (Ganache).

---

## 📦 Contenuto del repository

| Path                   | Descrizione                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `wallet_contract.sol`  | Smart‑contract Solidity 0.8.17 del Multi‑Sig Wallet                          |
| `wallet_main.py`       | Script Python che compila, deploya e interagisce con il contratto (Web3.py)  |
| `truffle/`             | Configurazione alternativa per deploy/test tramite **Truffle** + **Ganache** |
| `wallet_contract.json` | ABI + bytecode del contratto già compilato                                   |
| `.env`                 | Variabili d’ambiente (RPC URL e chiavi private)                              |
| `venv/`                | Ambiente virtuale Python (ignorato da git)                                   |

---

## ⚙️ Funzionalità implementate

### 🛠️ Setup & Ambiente

* Connessione a un nodo **Ganache** (HTTP RPC)
* Lettura di due chiavi private da `.env` e inizializzazione degli **owner**
* Verifica del `gasLimit` del blocco più recente

### 🏗️ Compilazione del contratto (`wallet_main.py`)

* Installazione automatica del compilatore **Solidity 0.8.17** (via `py‑solc‑x`) se mancante
* Estrazione di **ABI** e **bytecode** e serializzazione in `wallet_contract.json`

### 🚀 Deploy del Multi‑Sig Wallet

* Deploy con *N = 2* proprietari
* **`numConfirmationsRequired` parametrico** (nel test: 1)
* Stampa su console dell’indirizzo del contratto

### 💰 Operazioni sul Wallet

| Funzione                             | Scopo                                                   |
| ------------------------------------ | ------------------------------------------------------- |
| `receive()` *(payable)*              | Deposito ETH diretto da qualunque address               |
| `submitTransaction(to, value, data)` | Un owner propone una transazione                        |
| `confirmTransaction(txIndex)`        | Un owner approva la proposta (una sola volta)           |
| `executeTransaction(txIndex)`        | Esegue se `numConfirmations ≥ numConfirmationsRequired` |
| `getTransaction(txIndex)`            | Restituisce i dettagli di una transazione               |
| `getTransactionCount()`              | Numero di proposte totali                               |

> **Eventi emessi**: `SubmitTransaction`, `ConfirmTransaction`, `ExecuteTransaction`

### 🔄 Flusso dimostrativo (`wallet_main.py`)

1. **Finanziamento contratto** iniziale: 10 ETH inviati da `owners[0]` al contratto (`receive()`)
2. **Transfer standard**: 1 ETH da `owner A` → `owner B` (direct send)
3. **Flusso Multi‑Sig**

   1. `owner A` chiama `submitTransaction()` per inviare 5 ETH a sé stesso (solo a fini demo)
   2. `owner B` chiama `confirmTransaction()` sullo stesso indice
   3. `owner A` chiama `executeTransaction()` ➜ trasferimento on‑chain eseguito
4. Console log del saldo finale del contratto e degli eventi intercettati

### 🖼️ Output d’esempio

Sono inclusi screenshot di:

* **Terminale** (compilazione, deploy, transazioni)
* **Ganache UI** con i blocchi 0‑3 e le relative transazioni (Contract Creation, Value Transfer, Contract Call)

---

## ▶️ Esecuzione rapida

```bash
# 1 – Clona il repo
$ git clone https://github.com/BlackRaffo70/Wallet_Ethereum_Project.git
$ cd Wallet_Ethereum_Project

# 2 – Crea l’ambiente virtuale
$ python3 -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt  # oppure usa il comando qui sotto
$ pip install web3 python-dotenv py-solc-x

# 3 – Compila/Deploy/Interagisci
$ cp .env.example .env        # inserisci RPC e chiavi + nuovo gas limit(1200000 nel nostro caso)
$ ganache --gasLimit 12000000 # avvia Ganache
$ python wallet_main.py       # esegui lo script end‑to‑end
```

> **Truffle**:
>
> ```bash
> $ cd truffle && npm install
> $ truffle compile && truffle migrate
> ```

---

## 📂 Struttura del progetto (tree)

```
Eth_walletSIM/
├── wallet_main.py
├── wallet_contract.sol
├── wallet_contract.json
├── truffle/
│   └── ...
├── .env
└── venv/
```


