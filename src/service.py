import numpy as np
import bentoml
from bentoml import Context
from bentoml.io import JSON
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt

# Secret for JWT
SECRET_KEY = "my-super-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dummy login data
fake_user = {"username": "admin", "password": "admin"}

# JWT utility
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Input schema
class AdmissionInput(BaseModel):
    GRE_Score: float
    TOEFL_Score: float
    University_Rating: float
    SOP: float
    LOR: float
    CGPA: float
    Research: int

# Load model
model_ref = bentoml.sklearn.get("admissions_regression:latest")
model_runner = model_ref.to_runner()

svc = bentoml.Service("fabianloew_admissions_prediction", runners=[model_runner])

# Login endpoint
@svc.api(input=JSON(), output=JSON())
def login(credentials: dict):
    if credentials.get("username") == fake_user["username"] and credentials.get("password") == fake_user["password"]:
        token = create_access_token({"sub": credentials["username"]})
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Prediction endpoint
@svc.api(input=JSON(pydantic_model=AdmissionInput), output=JSON())
async def predict(input_data: AdmissionInput, context: Context):
    auth_header = context.request.headers.get("authorization")

    input_array = np.array([[
        input_data.GRE_Score,
        input_data.TOEFL_Score,
        input_data.University_Rating,
        input_data.SOP,
        input_data.LOR,
        input_data.CGPA,
        input_data.Research
    ]])

    prediction = await model_runner.predict.async_run(input_array)
    return {"chance_of_admit": prediction[0]}