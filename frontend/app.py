# python3.10 -m flask run
from flask import Flask, render_template, url_for, redirect, jsonify, request
# from forms import SettingsForm
import random
# from datetime import datetime,date
import threading
import queue
import time
from backend.basic_test import simulation
import json
from .forms import settingsForm
# from backend.ANSI import Colours


# Disabling Flask Logs
import logging
log = logging.getLogger('werkzeug') # This is the default flask logger
log.setLevel(logging.ERROR) # Filtered out any redundant logs like GETs, only logs when it's an error

app = Flask(__name__)
app.config["SECRET_KEY"] = "mmm-ice-cream-so-good"

# Simulation Stuff
input_queue = queue.Queue()  # Initialising input queue
def simulation_thead(): # This actually lets flask run and the simulation to run on a different thread
    simulation_thread = threading.Thread(
        target=simulation, args=(input_queue,))
    simulation_thread.daemon = True
    simulation_thread.start()
simulation_thead()

# variables
# user input from front end
is_default_mode = False
target_temperature = 20
is_fire_alarm = True

# system configuration for setting page
system_config = {
    'target_temperature': 25,
    'occupation_detect': False,
    'fire_alarm': False,
    'mode': 'Default Mode'
}

# Initialize JSON file and send target temperature data once, before anything else (so that we never receive an empty JSON file)
def initialize_target_data():
    target_data = {
        "target_temperature": target_temperature
    }
    with open("target_data.json", "w") as file:
        json.dump(target_data, file)

initialize_target_data()

# from backend
shared_data = {
    "is_occupied": True,
    "room1_temperature": 10,
    "room2_temperature": 12,
    "room3_temperature": 14,
    "room4_temperature": 16,
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


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for("homepage"))


@app.route("/homepage", methods=["GET", "POST"])
def homepage():

    with open("sensor_data.json", "r") as file:
        data = json.load(file)

    shared_data.update({
    "room1_temperature": data["room_temperatures"]["Living Room"],
    "room2_temperature": data["room_temperatures"]["Bathroom"],
    "room3_temperature": data["room_temperatures"]["Bedroom"],
    "room4_temperature": data["room_temperatures"]["Kitchen"],
    "current_temperature": int((data["room_temperatures"]["Living Room"] +data["room_temperatures"]["Bathroom"] +data["room_temperatures"]["Bedroom"] +data["room_temperatures"]["Kitchen"]) / 4),
    "is_occupied": data["occupancy_status"]
    })

    # If the request is an AJAX call, return JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        # response_data = {**shared_data, **target_data}
        # print("Response sent to AJAX", response_data)
        return jsonify(shared_data)
    
    return render_template("homepage.html",
                           is_default_mode=is_default_mode, target_temperature=target_temperature, is_fire_alarm=is_fire_alarm,
                           is_occupied=shared_data["is_occupied"],
                           current_temperature=shared_data["current_temperature"],
                           is_HVAC_on=shared_data["is_HVAC_on"],
                           HVAC_movement=shared_data["HVAC_movement"],
                           shared_data=shared_data)


@app.route("/rooms", methods=["GET", "POST"])
def rooms():

    with open("sensor_data.json", "r") as file:
        data = json.load(file)

    shared_data.update({
        "room1_temperature": data["room_temperatures"]["Living Room"],
        "room2_temperature": data["room_temperatures"]["Bathroom"],
        "room3_temperature": data["room_temperatures"]["Bedroom"],
        "room4_temperature": data["room_temperatures"]["Kitchen"],
        "current_temperature": int((data["room_temperatures"]["Living Room"] +data["room_temperatures"]["Bathroom"] +data["room_temperatures"]["Bedroom"] +data["room_temperatures"]["Kitchen"]) / 4),
        "is_occupied": data["occupancy_status"]
        })

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(shared_data)

        
    return render_template("rooms.html",
                           current_temperature=shared_data["current_temperature"],
                           room1_temperature=shared_data["room1_temperature"],
                           room2_temperature=shared_data["room2_temperature"],
                           room3_temperature=shared_data["room3_temperature"],
                           room4_temperature=shared_data["room4_temperature"],)   

# ROUTE FOR HANDLING TARGET TEMPERATURE CHANGES

@app.route('/set_target_temperature', methods=['POST'])
def set_target_temperature():
    # Changes to the target temperature (via the buttons) are directed here. We update the JSON file and our target_temperature global
    #   variable, with the latter being used (solely?) to update the target temperature in the UI
    new_temperature = request.form.get("target_temperature", type=int) # We pull the new target from the user input form and store it
    global target_temperature
    target_temperature = new_temperature

    target_data = {
        "target_temperature": new_temperature
    }
    with open("target_data.json", "w") as file:
        json.dump(target_data, file)

    # Redirect back to the homepage to be safe
    return redirect(url_for('homepage'))

@app.route("/settings",methods=["GET","POST"])
def settings(): 
    print("Inside settings route")

    form = settingsForm()
    if form.validate_on_submit():
        print("Form submitted") 

        # system_config.update({
        #     'target_temperature': form.target_temperature.data,
        #     'occupation_detect': form.occupation_detect.data,
        #     'fire_alarm': form.fire_alarm.data,
        #     'mode': form.mode.data
        # })
        
        system_config['target_temperature'] = form.target_temperature.data
        system_config['occupation_detect'] = form.occupation_detect.data
        system_config['fire_alarm'] = form.fire_alarm.data
        system_config['mode'] = form.mode.data
        print(form.fire_alarm.data)
        return redirect(url_for('homepage')) 


    return render_template("settings.html", form=form, system_config=system_config)   
