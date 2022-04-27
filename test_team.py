from locale import atoi
import requests
from sqlalchemy import true
BASE = "http://localhost:5000/"

print("To start adding people to the database, press enter.")
input()
while(True):
    name = input("Name of team: ")
    response = requests.put(BASE + "team/", {"name": name})
    print(response.json())
    input = input("Team added. Do you want to add more teams? (y/n)")
    print()
    if input == "n":
        break