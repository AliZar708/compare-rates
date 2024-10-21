from fastapi import HTTPException
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Helper function to connect to the database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            port=os.environ['DB_PORT']
        )
        return conn
    except Error as e:
        logging.error(f"Error connecting to the database: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

# Helper function to fetch rates for a specific date
def fetch_rates_by_date(date: str) -> List[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = '''
                    SELECT * FROM currency_rates WHERE DATE(`Date`) = %s
                '''
        cursor.execute(query, (date,))
        rates = cursor.fetchall()

        cursor.close()
        conn.close()
        return rates
    except Error as e:
        logging.error(f"Error fetching rates for date {date}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch currency rates.")
