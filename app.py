import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

db: Dict[str, dict] = {}  # In-memory storage for receipts and points

class Receipt(BaseModel):
    retailer: str
    purchaseDate: str  # YYYY-MM-DD
    purchaseTime: str  # HH:MM
    items: list  # List of dict with shortDescription and price
    total: str  # String to preserve decimal precision

def calculate_points(receipt: Receipt) -> int:
    points = 0
    logging.debug(f"Calculating points for receipt: {receipt}")
    
    # Rule 1: One point for every alphanumeric character in retailer name
    retailer_points = sum(c.isalnum() for c in receipt.retailer)
    points += retailer_points
    logging.debug(f"Retailer name points: {retailer_points}")
    
    # Rule 2: 50 points if total is a round dollar amount with no cents
    if float(receipt.total).is_integer():
        points += 50
        logging.debug("Added 50 points for round dollar amount")
    
    # Rule 3: 25 points if total is a multiple of 0.25
    if float(receipt.total) % 0.25 == 0:
        points += 25
        logging.debug("Added 25 points for total being a multiple of 0.25")
    
    # Rule 4: 5 points for every two items on the receipt
    item_points = (len(receipt.items) // 2) * 5
    points += item_points
    logging.debug(f"Added {item_points} points for items count")
    
    # Rule 5: Trimmed item description has even number of characters → 0.2 * price points
    for item in receipt.items:
        if len(item["shortDescription"].strip()) % 2 == 0:
            price_points = round(float(item["price"]) * 0.2)
            points += price_points
            logging.debug(f"Added {price_points} points for item: {item}")
    
    # Rule 6: Purchase date is odd → 6 points
    if int(receipt.purchaseDate.split('-')[-1]) % 2 == 1:
        points += 6
        logging.debug("Added 6 points for odd purchase date")
    
    # Rule 7: Purchase time is between 2PM and 4PM → 10 points
    purchase_time = datetime.strptime(receipt.purchaseTime, "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points += 10
        logging.debug("Added 10 points for purchase time between 2PM and 4PM")
    
    logging.debug(f"Total points calculated: {points}")
    return points

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    logging.info("Processing receipt request")
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    db[receipt_id] = {"receipt": receipt.model_dump(), "points": points}
    logging.info(f"Receipt processed with ID: {receipt_id} and points: {points}")
    return {"id": receipt_id}

@app.get("/receipts/{receipt_id}/points")
def get_points(receipt_id: str):
    logging.info(f"Fetching points for receipt ID: {receipt_id}")
    if receipt_id not in db:
        logging.warning("Receipt not found")
        raise HTTPException(status_code=404, detail="Receipt not found")
    points = db[receipt_id]["points"]
    logging.info(f"Points retrieved: {points}")
    return {"points": points}
