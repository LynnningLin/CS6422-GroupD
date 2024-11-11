# python3.10 -m flask run
from flask import Flask,render_template,url_for,redirect
# from forms import SettingsForm
import random
# from datetime import datetime,date
import threading
import queue
import time

app = Flask(__name__)

# variables
## user input from front end
is_default_mode=False
target_temperature=20
is_fire_alarm=True

## from backend
shared_data = {
    "is_occupied": True,
    "room1_temperature":10,
    "room2_temperature":12,
    "room3_temperature":14,
    "room4_temperature":16,
    "current_temperature": 13,
    "is_HVAC_on": False,
    "HVAC_movement": 1
}

# Function to update the variable 'a' every second
# def update_variable():
#     while True:
#         # Generate a new value for 'a' between 10 and 40
#         shared_data["current_temperature"] = random.randint(10, 40)
#         time.sleep(1)  # Wait for 1 second before updating again
# update_variable()

# routes
@app.route("/",methods=["GET","POST"])
def index(): 
    return redirect(url_for("homepage"))

@app.route("/homepage",methods=["GET","POST"])
def homepage(): 
    shared_data["room1_temperature"] = random.randint(10, 40)
    shared_data["room2_temperature"] = random.randint(10, 40)
    shared_data["room3_temperature"] = random.randint(10, 40)
    shared_data["room4_temperature"] = random.randint(10, 40)
    shared_data["current_temperature"] = int((shared_data["room1_temperature"]+shared_data["room2_temperature"]+shared_data["room3_temperature"]+shared_data["room4_temperature"])/4)
    return render_template("homepage.html",
                           is_default_mode=is_default_mode,target_temperature=target_temperature,is_fire_alarm=is_fire_alarm,
                            is_occupied=shared_data["is_occupied"],
                            current_temperature=shared_data["current_temperature"],
                            is_HVAC_on=shared_data["is_HVAC_on"],
                            HVAC_movement=shared_data["HVAC_movement"])    


@app.route("/rooms",methods=["GET","POST"])
def rooms(): 
    shared_data["room1_temperature"] = random.randint(10, 40)
    shared_data["room2_temperature"] = random.randint(10, 40)
    shared_data["room3_temperature"] = random.randint(10, 40)
    shared_data["room4_temperature"] = random.randint(10, 40)
    shared_data["current_temperature"] = int((shared_data["room1_temperature"]+shared_data["room2_temperature"]+shared_data["room3_temperature"]+shared_data["room4_temperature"])/4)

    return render_template("rooms.html",
                           current_temperature=shared_data["current_temperature"],
                           room1_temperature=shared_data["current_temperature"],
                           room3_temperature=shared_data["current_temperature"],
                           room2_temperature=shared_data["current_temperature"],
                           room4_temperature=shared_data["current_temperature"],)   


@app.route("/settings",methods=["GET","POST"])
def settings(): 

    return render_template("settings.html")   
