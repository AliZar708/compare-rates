# Currency Exchange Rates API

This project is a **FastAPI** application that tracks currency exchange rates and compares the current day's rates with the previous day's rates for a list of currencies.

## Endpoint
Here is the deployed endpoint.
https://zqzsrqthyl7zgrqyob2dnoaapq0qpiua.lambda-url.eu-north-1.on.aws/rates/compare
App is deployed on AWS Lambda

## Features

- Fetches and stores daily currency exchange rates from European Central Bank data.
- Provides a REST API to return current exchange rates and compares them to the previous day.
- Built with **FastAPI** and deployed using **AWS Lambda** with **Mangum**.

## Note:
- The live data was not available so i have pushed .csv to the rds MYSQL.
- The date is hard coded at as the last date in my data is 16 oct 2024. so it shows the difference of rates between 15 and 16 oct, but it can be changed easyilt when live data fetching is available.
## Table of Contents

1. [Installation](#installation)
2. [API Endpoints](#api-endpoints)
3. [Error Handling](#error-handling)
4. [Logging](#logging)
5. [Testing](#testing)

---

## Installation

### Prerequisites

- Python 3.8

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/AliZar708/ali-zar-assesment
   cd ali-zar-assesment

2. Install dependencies:
pip install -r requirements.txt

3. Run the application:
uvicorn app:app --reload

## API Endpoints

### Root Endpoint

**GET** `/`

**Purpose**: Returns a welcome message.

#### Example Response:
```json
{
  "message": "Currency Rates API"
}
```
### Get Current and Previous Day Rates

**GET** `/rates/compare`

**Purpose**: Returns the current day's exchange rates and compares them with the previous day's rates.

#### Example Response:
```json
{
    "date": "2024-10-17",
    "comparisons": [
        {
            "currency": "USD",
            "current_rate": 1.0897,
            "previous_rate": 1.0873,
            "rate_change_percentage": 0.2209
        },
        {
            "currency": "JPY",
            "current_rate": 162.57,
            "previous_rate": 162.45,
            "rate_change_percentage": 0.0739
        }
    ]
}
```
## Running Tests

This project includes unit tests for testing the FastAPI endpoints. The tests are written using `pytest` and can be run using the following steps:

### Prerequisites

Before running the tests, make sure you have the required dependencies installed. You can install them using `pip`:

```bash
pip install pytest pytest-mock fastapi testclient
```
## Running the Tests
To run the tests, execute the following command in the root of your project:
```bash
pytest
```