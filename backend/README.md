# Altron Backend

Handles the business logic for Altron.

## Usage

**Run Locally**
```bash
uvicorn src.main:app --reload
```

**Run on Docker**
```bash
docker build -t altron-backend .
docker run -p 8000:8000 altron-backend
```