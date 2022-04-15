import requests
#
BASE = "http://localhost:5000/"

response = requests.patch(BASE + "video/2", {})
print(response.json())