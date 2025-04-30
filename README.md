# ADMISSIONS PREDICTION API - BENTOML & DOCKER

**Author**: Fabian Loew  
**Project**: BentoML Exam – Containerized API for Predicting University Admission Chances

---

## PROJECT OVERVIEW

This project delivers a containerized BentoML API that predicts the chance of university admission based on student features.  
The model is trained using a regression algorithm on historical admissions data.

The API includes:
- A `/login` endpoint secured with JWT for authentication.
- A `/predict` endpoint that returns the admission chance.
- A containerized BentoML service using Docker.

---

## PREREQUISITES & SETUP

Before building or running, ensure you have:
- Python 3.x installed.
- Docker Desktop (or Docker Engine/CLI) installed and running.
- The project files downloaded or cloned.

### Setup Steps

1. **Navigate to the Project Root**  
   Open your terminal and change to the `examen_bentoml` directory (the one containing `src/`, `data/`, `bentofile.yaml`, etc.).

   ```bash
   cd /path/to/your/BentoML_Exam/examen_bentoml
   ```

2. **Create and Activate Virtual Environment (Recommended)**
   ```bash
   python3 -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**
   Install the main packages required for local development, testing, and building the Bento. `pip` will handle installing their dependencies automatically.
   ```bash
   pip install numpy pandas scikit-learn bentoml pydantic python-jose[cryptography] pytest requests fastapi
   ```

4. **Prepare Data**  
   Run the script to split the raw data into training and testing sets.

   ```bash
   python src/prepare_data.py
   ```

5. **Train and Save Model**  
   Run the training script to train the model and save it to the local BentoML model store with the tag `admissions_regression:latest`.

   ```bash
   python src/train_model.py
   ```

---

## PART 1: BUILD BENTO & DOCKER IMAGE

*Ensure you are in the `examen_bentoml` directory and your virtual environment is active.*

1. **Build the Bento**  
   Package the service code, model, and dependencies into a Bento.

   ```bash
   bentoml build
   ```

   This uses the configuration in `bentofile.yaml`. Note the output tag (e.g., `fabianloew_admissions_prediction:<VERSION>`).

2. **Containerize the Bento**

   ```bash
   bentoml containerize fabianloew_admissions_prediction:latest
   ```

   
   This creates a Docker image. **Note the specific version tag** output by this command (e.g., `fabianloew_admissions_prediction:ovo36xa7hswv5lg6`). You will need this tag for the next steps.

---

## PART 2: RUN CONTAINER & TEST API

1. **Load Docker Image (if provided as tar file)**

   ```bash
   docker load -i bento_image.tar
   ```

2.  **Run the Container** 

    Replace `<VERSION_TAG>` below with the specific tag you noted from the `bentoml containerize` output (e.g., `gjbyblrbsoy45lg6`).
    ```bash
    docker run --rm -p 3000:3000 fabianloew_admissions_prediction:<VERSION_TAG>
    ```
    The service will be accessible at http://localhost:3000. Keep this terminal running.

3. **Get an Access Token (Authentication)**
   Before you can use the /predict endpoint, you need to authenticate via the /login endpoint to get a temporary access token (JWT). Open a new terminal window and run the following curl command:
   ```
    curl -X POST \
      -H "Content-Type: application/json" \
      -d '{
         "username": "admin",
         "password": "admin"
          }' \
    http://localhost:3000/login
   ```


   **Expected Output and Action**:
   You will receive a JSON response containing the token:
   ```
   {"access_token":"<SOME_LONG_JWT_TOKEN_STRING>"}
   ```
   Copy the actual token string (the value associated with the "access_token" key, without the quotes) from the response. You'll need it in the next step.

4. **CMake the Prediction Request**
Now, use the token you just copied to make an authorized request to the /predict endpoint. Replace <YOUR_TOKEN_HERE> in the command below with the actual token you copied.

   ```
       curl -X POST \
      -H "Authorization: Bearer <YOUR_TOKEN_HERE>" \
      -H "Content-Type: application/json" \
      -d '{
            "GRE_Score": 330.0,
            "TOEFL_Score": 110.0,
            "University_Rating": 4.0,
            "SOP": 4.8,
            "LOR": 4.5,
            "CGPA": 9.5,
            "Research": 1
          }' \
      http://localhost:3000/predict
    
   ```

   **Expected Output:**:
   You should receive the prediction result
   ```json
   
   {"chance_of_admit":[0.901049...]}
        
   ```

5. **Run Unit Tests**

   ```bash
   pytest src/tests/test_service.py -v
   ```

---

## PROJECT STRUCTURE

```
.
├── data/
│   ├── raw/
│   │   └── admission.csv       # Original dataset
│   └── processed/              # Output of prepare_data.py
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
├── src/
│   ├── prepare_data.py         # Data splitting script
│   ├── train_model.py          # Model training & saving script
│   ├── service.py              # BentoML API service definition
│   └── tests/
│       └── test_service.py     # Pytest unit/integration tests
├── venv/                       # Virtual environment (if created)
├── bentofile.yaml              # BentoML build configuration
└── README.md                   # This file
```

---

## PYTHON DEPENDENCIES

**Core Build/Run Dependencies (defined in `bentofile.yaml`):**
- numpy
- pandas
- scikit-learn
- bentoml
- pydantic
- python-jose

**Local Setup/Testing Dependencies:**
- pytest
- requests

These are installed during the setup step using `pip install ...`.
