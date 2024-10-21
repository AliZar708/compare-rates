import pytest
from fastapi.testclient import TestClient
from app import app  # Import your FastAPI app from your app module

client = TestClient(app)

# Test the root endpoint
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Currency Rates API"}

# Test the /rates/compare endpoint when data exists
def test_rates_compare_success(mocker):
    # Mock the database response to simulate existing data for today and the previous day
    mock_today_data = [{"USD": 1.0897, "JPY": 162.57, "Date": "2024-10-16"}]
    mock_yesterday_data = [{"USD": 1.0873, "JPY": 162.45, "Date": "2024-10-15"}]

    mocker.patch('app.fetch_rates_by_date', side_effect=[mock_today_data, mock_yesterday_data])

    response = client.get("/rates/compare")
    assert response.status_code == 200
    data = response.json()
    
    # Update the expected date to match the mock data
    assert data["date"] == "2024-10-16"
    assert len(data["comparisons"]) > 0
    assert data["comparisons"][0]["currency"] == "USD"
    assert data["comparisons"][0]["current_rate"] == 1.0897
    assert data["comparisons"][0]["previous_rate"] == 1.0873


# Test the /rates/compare endpoint when no data exists
def test_rates_compare_no_data(mocker):
    mocker.patch('app.fetch_rates_by_date', return_value=[])
    
    response = client.get("/rates/compare")
    assert response.status_code == 404
    assert response.json() == {"detail": "No rates found for today."}

# Test the /rates/compare endpoint when only today's data is missing
def test_rates_compare_missing_today(mocker):
    mock_yesterday_data = [{"USD": 1.0873, "JPY": 162.45, "Date": "2024-10-16"}]
    
    mocker.patch('app.fetch_rates_by_date', side_effect=[[], mock_yesterday_data])
    
    response = client.get("/rates/compare")
    assert response.status_code == 404
    assert response.json() == {"detail": "No rates found for today."}

# Test the /rates/compare endpoint when only yesterday's data is missing
def test_rates_compare_missing_yesterday(mocker):
    mock_today_data = [{"USD": 1.0897, "JPY": 162.57, "Date": "2024-10-17"}]
    
    mocker.patch('app.fetch_rates_by_date', side_effect=[mock_today_data, []])
    
    response = client.get("/rates/compare")
    assert response.status_code == 404
    assert response.json() == {"detail": "No rates found for the previous day."}
