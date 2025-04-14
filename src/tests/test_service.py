import pytest
import requests
from datetime import datetime, timedelta
import jwt

# Set up base URL
BASE_URL = "http://localhost:3000"

# Set up test credentials
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"
INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_pass"
JWT_SECRET_KEY = "your_secret_key"  # Replace this with your actual JWT secret key

# Utility function to create a valid token (you can adjust this based on your setup)
def create_valid_token():
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": VALID_USERNAME,
        "exp": expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

# 1. JWT Authentication Test

def test_auth_missing_token():
    response = requests.get(f"{BASE_URL}/predict")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_auth_invalid_token():
    invalid_token = "invalid_token"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = requests.get(f"{BASE_URL}/predict", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_auth_valid_token():
    valid_token = create_valid_token()
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = requests.get(f"{BASE_URL}/predict", headers=headers)
    assert response.status_code == 200

# 2. Login API Test

def test_login_valid_credentials():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": VALID_USERNAME,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": INVALID_USERNAME,
        "password": INVALID_PASSWORD
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

# 3. Prediction API Test

def test_predict_missing_token():
    response = requests.post(f"{BASE_URL}/predict", json={
        "GRE_Score": 330,
        "TOEFL_Score": 110,
        "University_Rating": 4,
        "SOP": 4.8,
        "LOR": 4.5,
        "CGPA": 9.5,
        "Research": 1
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_predict_invalid_token():
    invalid_token = "invalid_token"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = requests.post(f"{BASE_URL}/predict", headers=headers, json={
        "GRE_Score": 330,
        "TOEFL_Score": 110,
        "University_Rating": 4,
        "SOP": 4.8,
        "LOR": 4.5,
        "CGPA": 9.5,
        "Research": 1
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_predict_valid_data():
    valid_token = create_valid_token()
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = requests.post(f"{BASE_URL}/predict", headers=headers, json={
        "GRE_Score": 330,
        "TOEFL_Score": 110,
        "University_Rating": 4,
        "SOP": 4.8,
        "LOR": 4.5,
        "CGPA": 9.5,
        "Research": 1
    })
    assert response.status_code == 200
    assert "chance_of_admit" in response.json()

def test_predict_invalid_data():
    valid_token = create_valid_token()
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = requests.post(f"{BASE_URL}/predict", headers=headers, json={
        "GRE_Score": "invalid_data",
        "TOEFL_Score": 110,
        "University_Rating": 4,
        "SOP": 4.8,
        "LOR": 4.5,
        "CGPA": 9.5,
        "Research": 1
    })
    assert response.status_code == 400
    assert "detail" in response.json()
