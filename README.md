# 🎓 Admissions Prediction API 
- 
- BentoML & DockerAuthor: Fabian LoewProject: BentoML Exam – Containerized API for Predicting University Admission Chances📦 Project OverviewThis project delivers a containerized BentoML API that predicts the chance of university admission based on student features.The model is trained using a regression algorithm on historical admissions data.The API includes:A /login endpoint secured with JWT for authentication.A /predict endpoint that returns the admission chance.A containerized BentoML service using Docker.🛠️ Part 1: Build and Package the API1. (Optional) Create or Rebuild the BentoIf not done already, you can build the Bento from source:bentoml build
This uses the configuration in bentofile.yaml.2. Containerize the BentoBuild the Docker image from the Bento:bentoml containerize fabianloew_admissions_prediction:latest
This creates a Docker image named fabianloew_admissions_prediction:latest.🧪 Part 2: Run the Container and Test the API1. Load Docker Image (if provided as tar file)If the image was submitted as bento_image.tar, load it with:docker load -i bento_image.tar
2. Run the ContainerStart the container and expose the API on port 3000:docker run --rm -p 3000:3000 fabianloew_admissions_prediction:latest
You should now see BentoML start the service at http://localhost:3000.3. Authenticate to Get Access TokenMake a POST request to /login to retrieve a JWT access token:POST http://localhost:3000/loginBody:{
  "username": "admin",
  "password": "admin"
}
Response:{
  "access_token": "<JWT_TOKEN>"
}
4. Call the Prediction EndpointUse the token from /login to call /predict:POST http://localhost:3000/predictHeaders:Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Body:{
  "GRE": 330,
  "TOEFL": 110,
  "UniversityRating": 4,
  "SOP": 4.5,
  "LOR": 4.8,
  "CGPA": 9.5,
  "Research": 1
}
Expected response:{
  "chance_of_admit": [0.90]
}
✅ Run Unit TestsWith the API running on localhost:3000, execute:python3 -m pytest tests/test_service.py
All tests should pass with PASSED status.🗂️ Project Structure.
├── src/
│   ├── service.py         # BentoML API service
│   └── test_api.py        # Manual API test
├── tests/
│   └── test_service.py      # Unit tests
├── bentofile.yaml           # BentoML build config
├── bento_image.tar          # Exported Docker image
└── README.md                # This file
📤 Export Docker Image for SubmissionMake sure the Docker image name follows the required format:docker save -o bento_image.tar fabianloew_admissions_prediction:latest
⚠️ Use this exact format: <yourname>_<imagename> → fabianloew_admissions_prediction📦 Python DependenciesEnsure the following are included in bentofile.yaml:    numpy
    pandas
    scikit-learn
    bentoml
    pydantic
    requests
    python-jose
