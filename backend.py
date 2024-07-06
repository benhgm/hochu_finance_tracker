import logging
from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from database import get_session, Transaction, create_user_database

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class TransactionsCreate(BaseModel):
    user: List[str]
    item: List[str]
    mode_of_payment: List[str]
    credit_card: List[str]
    category: List[str]
    amount: List[float]
    date: List[str]

    def validate_transactions(self):
        lengths = [
            len(self.item),
            len(self.mode_of_payment),
            len(self.category),
            len(self.amount),
            len(self.date),
        ]
        if len(set(lengths)) != 1:
            raise ValueError("All fields must have the same number of entries")
        if len(set(self.user)) != 1:
            raise ValueError("Only can add transactions for a single user")
    
    def convert_dates(self):
        self.date = [datetime.strptime(d, '%d-%m-%Y').date() for d in self.date]

@app.post("/transactions/")
async def create_transactions(transactions: TransactionsCreate):
    try:
        transactions.validate_transactions()
        transactions.convert_dates()
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    logger.info(f"Creating database for user: {transactions.user}")
    create_user_database(transactions.user[0])  # Ensure the database exists
    db = get_session(transactions.user[0])

    db_transactions = [
        Transaction(
            item=item,
            mode_of_payment=mode,
            credit_card=card,
            category=category,
            amount=amount,
            date=date
        )
        for item, mode, card, category, amount, date in zip(
            transactions.item,
            transactions.mode_of_payment,
            transactions.credit_card,
            transactions.category,
            transactions.amount,
            transactions.date
        )
    ]

    db.add_all(db_transactions)
    db.commit()
    
    return {"detail": "Transactions added successfully"}
