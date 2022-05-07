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
    return redirect("/login")

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
        api_call = requests.get(BASE + "person/" + str(firstname) + "_" + str(lastname)).json()
        if api_call == {"error": 404}:
            return render_template("apology.html", message="Person not found")

        person_id = int(api_call["id"])

        # Remember which user has logged in
        session["person_id"] = person_id

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
        elif not request.form.get("role"):
            return render_template("apology.html", message="Role is required")
        elif not request.form.get("age"):
            return render_template("apology.html", message="Age is required")
        
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        role = request.form.get("role")
        age = request.form.get("age")
        requests.put(BASE + "person/", {"firstname": firstname, "lastname": lastname, "age": age, "role": role})
        return redirect("/login")
    else:
        return render_template("register.html")


#if __name__ == '__main__':
#    app.run(host = "localhost", port=5012, debug=True)

