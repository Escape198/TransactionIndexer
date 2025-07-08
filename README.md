# Ethereum Transaction Indexer

This project is a FastAPI-based service that indexes Ethereum transactions for a specific address and stores them in PostgreSQL.  
It provides API endpoints to index transactions, query them, delete them, and get aggregated statistics.

---

## 🚀 Features

- Index transactions between specific blocks.
- Filter transactions by date and minimum value.
- Delete indexed transactions.
- Get summary statistics per address.

---

## 🛠️ Requirements

- Python 3.10+
- PostgreSQL
- Docker (optional)


## 🧩 Installation
- Set environment variables in .env:
  ```ini
  DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tx_indexer
  ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
  ```

## 🐳 Running with Docker
```bash
docker-compose up --build
```

## Test
Index Transactions
Index all transactions for USDT contract between two block numbers:
```bash
curl -X POST "http://localhost:8000/api/v1/index/0xdAC17F958D2ee523a2206206994597C13D831ec7?start_block=19000000&end_block=19000001"
```

Response:
```json
{
  "indexed": [
    {
      "hash": "...",
      "from_address": "...",
      "to_address": "...",
      "value": "...",
      "timestamp": "...",
      "logs": [...]
    }
  ]
}
```
