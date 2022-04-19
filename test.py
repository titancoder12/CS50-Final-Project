import requests
BASE = "http://localhost:5000/"

response = requests.put(BASE + "person/4", {"name":"Shohei", "age": 25})
print(response.json())
input()
response = requests.get(BASE + "person/4")
print(response.json())