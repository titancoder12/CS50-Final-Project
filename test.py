import requests
BASE = "http://localhost:5000/"

response = requests.get(BASE + "Joe/1")
print(response.json())