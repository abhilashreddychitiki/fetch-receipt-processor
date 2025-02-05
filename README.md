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

## API Endpoints

### Submit a Receipt

`POST /receipts/process`

#### Example Request:

```json
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    { "shortDescription": "Gatorade", "price": "2.25" },
    { "shortDescription": "Gatorade", "price": "2.25" }
  ],
  "total": "4.50"
}
```

### Retrieve Points for a Receipt

`GET /receipts/{receipt_id}/points`

#### Example Response:

```json
{
  "points": 75
}
```
