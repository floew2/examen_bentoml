# 🎓 Admissions Prediction API - BentoML & Docker

Author: Fabian Loew  
Project: BentoML Exam – Containerized API for Predicting University Admission Chances

---

## 📦 Project Overview

This project delivers a containerized BentoML API that predicts the **chance of university admission** based on several student features. The model is trained using a regression algorithm on historical admissions data.

The API includes:
- A login endpoint secured with JWT.
- A prediction endpoint that returns the admission chance.
- A fully containerized environment using BentoML and Docker.

---

```bash       
├── examen_bentoml          
│   ├── data       
│   │   ├── processed      
│   │   └── raw           
│   ├── models      
│   ├── src       
│   └── README.md
```

## 🚀 How to Run the Project

### 1️⃣ Decompress the Docker Image

If you're starting from the provided image archive (`bento_image.tar`), load it into Docker:

```bash
docker load -i bento_image.tar

```
### 2️⃣ Run the Container

Start the API container on port 3000:
```bash
docker run --rm -p 3000:3000 fabianloew_admissions_prediction:latest

```
Once running, the API will be available at:
```bash
http://localhost:3000