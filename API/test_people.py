from locale import atoi
import requests
from sqlalchemy import true
BASE = "http://localhost:5000/"

print("To start adding people to the database, press enter.")
input()
first_name, last_name, age, role = "", "", "", ""
while(True):
    first_name = input("First name of person: ")
    last_name = input("Last name of person: ")
    age = atoi(input("Age of person: "))
    role = input("Role of person: ")

    response = requests.put(BASE + "person/", {"firstname":first_name, "lastname":last_name, "role":role, "team_id":1, "age":age})
    print(response.json())

# Add a person:
# curl -X PUT -d name=bar -d age=1 http://localhost:5000/person/

# Get a person:
# curl http://localhost:5000/person/0