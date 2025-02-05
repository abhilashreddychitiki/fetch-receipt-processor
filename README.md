# Receipt Processor API

This is a FastAPI-based application for processing receipts and calculating reward points.

## Setup & Running Locally

### Using Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

## Running Tests

```sh
pytest tests/
```
