import requests

url = "http://localhost:3000/predict"
headers = {"Content-Type": "application/json"}
data = {
  "GRE_Score": 330,
  "TOEFL_Score": 110,
  "University_Rating": 4,
  "SOP": 4.8,
  "LOR": 4.5,
  "CGPA": 9.5,
  "Research": 1
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
