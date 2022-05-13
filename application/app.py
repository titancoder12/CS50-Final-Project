import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import requests

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

BASE = "http://localhost:5000/"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("firstname"):
            return render_template("apology.html", message="First name is required")
        elif not request.form.get("lastname"):
            return render_template("apology.html", message="Last name is required")
        
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        response = requests.get(BASE + "person/" + str(firstname) + "_" + str(lastname)).json()
        if response == {"error": 404}:
            return render_template("apology.html", message="Person not found")

        person_id = int(response["id"])

        # Remember which user has logged in
        session["person_id"] = person_id
        session["team_id"] = int(response["team_id"])
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["role"] = response["role"]
        session["age"] = response["age"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        if not request.form.get("firstname"):
            return render_template("apology.html", message="First name is required")
        elif not request.form.get("lastname"):
            return render_template("apology.html", message="Last name is required")
        elif not request.form.get("age"):
            return render_template("apology.html", message="Age is required")
        elif not request.form.get("role"):
            return render_template("apology.html", message="Role is required")
        
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        age = request.form.get("age")
        role = request.form.get("role")
        response = requests.put(BASE + "person/", {"firstname": firstname, "lastname": lastname, "age": age, "role": role, "team_id": 0}).json()
        session["person_id"] = int(response["id"])
        session["team_id"] = int(response["team_id"])
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["role"] = role
        session["age"] = age
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/teams", methods=["GET", "POST"])
def teams():
    team_id = 0
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return render_template("apology.html", message="Name of team is required")
        team_id = requests.put(BASE + "team/", {"name": name}).json()#team_id = requests.put(BASE + "team/", {"name": name})
        print("à23545456776234e56523534534543534534545345435435435345345345435435         " + str(team_id))
        requests.patch(BASE + "person/" + str(session["person_id"]), {"team_id": team_id})
        session["team_id"] = int(team_id)
        return redirect('/teams')
    else:
        firstname = session["firstname"]
        lastname = session["lastname"]
        url = BASE + "person/" + firstname + "_" + lastname
        print(f"Trying to do GET to {url}")
        response = requests.get(url).json()
        team_id = response["team_id"]
        print(f"The response is: {str(response)} ")
        print(response["team_id"])
        if int(team_id) == 0:
            return render_template("teams.html", people={}, name="No Teams")
        team_id = str(response["team_id"])
        team = requests.get(BASE + "team/" + team_id).json()
        name = team["name"]
        team.pop("name")
        id = team["id"]
        team.pop("id")
        people = team.copy()
        return render_template("teams.html", people=people, name=name)
        
@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        role = request.form.get("role")
        age = request.form.get("age")
        team_id = str(request.form.get("team_id"))
        person_id = int(session["person_id"])
        if not firstname:
            return render_template("apology.html", message="Firstname is required")
        elif not lastname:
            return render_template("apology.html", message="Lastname is required")
        elif not role:
            return render_template("apology.html", message="Role is required")
        elif not age:
            return render_template("apology.html", message="Age is required")
        elif not team_id:
            return render_template("apology.html", message="Team id is required")
        response = requests.get(BASE + "team/" + team_id).json()
        if response == {"message": 404}:
            return render_template("apology.html", message="Team id does not exist")
        
        requests.patch(BASE + "person/" + str(person_id), {"firstname":firstname, "lastname":lastname, "role":role, "age":str(age), "team_id":str(team_id)})
        session["firstname"] = firstname
        session["lastname"] = lastname
        session["role"] = role
        session["age"] = age
        session["team_id"] = team_id
        return render_template("account.html", firstname=firstname, lastname=lastname, role=role, age=age, team_id=int(team_id))
    else:
        return render_template("account.html", firstname=session["firstname"], lastname=session["lastname"], role=session["role"], age=session["age"], team_id=int(session["team_id"]))
