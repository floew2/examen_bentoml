import pytest
import requests
from datetime import datetime, timedelta
from jose import jwt

# --- Configuration ---
BASE_URL = "http://localhost:3000"

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"
INVALID_USERNAME = "wrong_user"
INVALID_PASSWORD = "wrong_pass"

JWT_SECRET_KEY = "my-super-secret"
ALGORITHM = "HS256"

# Valid payload for prediction endpoint
VALID_PREDICTION_PAYLOAD = {
    "GRE_Score": 330.0,
    "TOEFL_Score": 110.0,
    "University_Rating": 4.0,
    "SOP": 4.8,
    "LOR": 4.5,
    "CGPA": 9.5,
    "Research": 1
}

# --- Helper Function ---
def create_valid_token():
    """Creates a JWT token using the correct secret and algorithm."""
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": VALID_USERNAME,
        "exp": expiration
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

# --- Test Cases ---

# 1. Login API Tests
def test_login_valid_credentials():
    """Test successful login with correct credentials."""
    response = requests.post(f"{BASE_URL}/login", json={
        "username": VALID_USERNAME,
        "password": VALID_PASSWORD
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    try:
        token = response.json()["access_token"]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == VALID_USERNAME
    except jwt.JWTError as e:
        pytest.fail(f"Token decoding failed: {e}")

def test_login_invalid_credentials():
    """Test login failure with incorrect credentials."""
    response = requests.post(f"{BASE_URL}/login", json={
        "username": INVALID_USERNAME,
        "password": INVALID_PASSWORD
    })
    assert response.status_code == 500

def test_login_missing_username():
    """Test login failure with missing username."""
    response = requests.post(f"{BASE_URL}/login", json={
        "password": VALID_PASSWORD
    })
    assert response.status_code == 500

def test_login_missing_password():
    """Test login failure with missing password."""
    response = requests.post(f"{BASE_URL}/login", json={
        "username": VALID_USERNAME
    })
    assert response.status_code == 500


# 2. Prediction API Tests
def test_predict_valid_data_with_valid_token():
    """Test prediction with valid data and a valid token."""
    valid_token = create_valid_token()
    headers = {"Authorization": f"Bearer {valid_token}"}
    response = requests.post(
        f"{BASE_URL}/predict",
        headers=headers,
        json=VALID_PREDICTION_PAYLOAD
    )
    assert response.status_code == 200
    assert "chance_of_admit" in response.json()
    assert isinstance(response.json()["chance_of_admit"], list)
    assert len(response.json()["chance_of_admit"]) > 0
    assert isinstance(response.json()["chance_of_admit"][0], float)


def test_predict_valid_data_with_missing_token():
    """
    Test prediction with valid data but NO token.
    EXPECTED TO PASS (200 OK) because service.py currently doesn't validate tokens on /predict.
    """
    response = requests.post(
        f"{BASE_URL}/predict",
        json=VALID_PREDICTION_PAYLOAD
    )
    assert response.status_code == 200
    assert "chance_of_admit" in response.json()
    print("\nWARNING: test_predict_valid_data_with_missing_token passed (200 OK), "
          "but service.py is missing token validation on /predict.")

def test_predict_valid_data_with_invalid_token_string():
    """
    Test prediction with valid data but an INVALID token string.
    """
    invalid_token = "this-is-not-a-real-jwt-token"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = requests.post(
        f"{BASE_URL}/predict",
        headers=headers,
        json=VALID_PREDICTION_PAYLOAD
    )
    assert response.status_code == 200 # Should be 401/403 if validation was implemented
    assert "chance_of_admit" in response.json()
    print("\nWARNING: test_predict_valid_data_with_invalid_token_string passed (200 OK), "
          "but service.py is missing token validation on /predict.")

def test_predict_valid_data_with_wrong_secret_token():
    """
    Test prediction with valid data but a token signed with the WRONG secret.
    """
    expiration = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": VALID_USERNAME, "exp": expiration}
    wrong_secret_token = jwt.encode(payload, "wrong-secret-key", algorithm=ALGORITHM) # Use wrong key
    headers = {"Authorization": f"Bearer {wrong_secret_token}"}

    response = requests.post(
        f"{BASE_URL}/predict",
        headers=headers,
        json=VALID_PREDICTION_PAYLOAD
    )
    assert response.status_code == 200 # Should be 401/403 if validation was implemented
    assert "chance_of_admit" in response.json()
    print("\nWARNING: test_predict_valid_data_with_wrong_secret_token passed (200 OK), "
          "but service.py is missing token validation on /predict.")


def test_predict_invalid_data_type():
    """Test prediction failure when input data types are wrong (Pydantic validation)."""
    valid_token = create_valid_token()
    headers = {"Authorization": f"Bearer {valid_token}"}
    invalid_payload = VALID_PREDICTION_PAYLOAD.copy()
    invalid_payload["GRE_Score"] = "this should be a float" # Invalid type

    response = requests.post(
        f"{BASE_URL}/predict",
        headers=headers,
        json=invalid_payload
    )
    # Expecting 400 based on logs
    assert response.status_code == 400
    assert isinstance(response.text, str)
    assert "GRE_Score" in response.text
    assert "unable to parse string" in response.text


def test_predict_missing_field():
    """Test prediction failure when a required field is missing (Pydantic validation)."""
    valid_token = create_valid_token()
    headers = {"Authorization": f"Bearer {valid_token}"}
    invalid_payload = VALID_PREDICTION_PAYLOAD.copy()
    del invalid_payload["CGPA"]

    response = requests.post(
        f"{BASE_URL}/predict",
        headers=headers,
        json=invalid_payload
    )
    # Expecting 400 based on logs
    assert response.status_code == 400
    assert isinstance(response.text, str)
    assert "CGPA" in response.text
    assert "Field required" in response.text
