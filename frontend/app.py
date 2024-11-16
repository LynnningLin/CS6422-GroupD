from flask import Flask,render_template,url_for,redirect
# from forms import SettingsForm
import random
# from datetime import datetime,date
import threading
import queue
import time
from backend.basic_test import HVAC, Medium, Node, TemperatureSensor, MotionSensor
import simpy.rt
from flask_socketio import SocketIO, emit

# from backend.ANSI import Colours

app = Flask(__name__) 
socketIO = SocketIO(app) # Still working on this, this is to allowd real realtime updates on the browserß

# Simulation/Instances Stuff
input_queue = queue.Queue() # Initialising input queue 
simulation_instance = {} # this is where we will store all instances from the simulation
hvac_event = threading.Event()  # This will help synchronize access to hvac --> Threading events won't be mismatched 


# //// SIMULATION INIT \\\\ #
def simulation(): # Running the simulation through the flask app.py instead of directly in the simulation file
    env = simpy.rt.RealtimeEnvironment(factor=0.01, strict=False) # set "strict" to False, now simulation can be "too slow" without throwing errors
    medium = Medium(env)

    HVAC(env, medium, 'Actuator', 'A001')
    TemperatureSensor(env, medium, 'Living Room', 'T-Sensor', 'TS001')
    TemperatureSensor(env, medium, 'Bathroom', 'T-Sensor', 'TS002')
    TemperatureSensor(env, medium, 'Bedroom', 'T-Sensor', 'TS003')
    TemperatureSensor(env, medium, 'Kitchen', 'T-Sensor', 'TS004')
    MotionSensor(env, medium, 'Home', 'M-Sensor', 'MS001')


    # Storing Instances
    hvac = HVAC(env, medium, 'Actuator', 'A001') # getting hvac instance
    simulation_instance['hvac'] = hvac # storing hvac instance as a global variable in the simulation dict

    print(f'HVAC instance stored in simulation instance Dict {simulation_instance}') # some debugging to see if the hvac was actually stored in the dict
    hvac_event.set() # Signal that HVAC is initialized

    env.run() # just changed this where the simulation will run indefinitely

# This actually lets flask run and the simulation to run on a different thread
def simulation_thead():
    simulation_thread = threading.Thread(target=simulation)
    simulation_thread.daemon = True
    simulation_thread.start()
simulation_thead()




# variables
## user input from front end
is_default_mode=False
target_temperature=20
is_fire_alarm=True

## from backend
shared_data = {
     "is_occupied": True,
        "room1_temperature":13,
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


# @socketIO.on('connect')
# def handle_connection():
#     return emit_room_temps()

# def emit_room_temps():
#     if "hvac" in simulation_instance:
#         hvac_instance = simulation_instance["hvac"]
#         room_temp = hvac_instance.get_room_temp()  # Retrieve room temperatures
#         current_temperature = (room_temp.get("Living Room", 10) + room_temp.get("Bathroom", 12) +
#                                room_temp.get("Bedroom", 14) + room_temp.get("Kitchen", 16)) / 4
#         shared_data = {
#             "room1_temperature": room_temp.get("Living Room", 10),
#             "room2_temperature": room_temp.get("Bathroom", 12),
#             "room3_temperature": room_temp.get("Bedroom", 14),
#             "room4_temperature": room_temp.get("Kitchen", 16),
#             "current_temperature": round(current_temperature, 1)
#         }
#         socketio.emit('update_room_temperatures', shared_data)

# @app.route("/update_temperatures")
# def update_temperatures():
#     # Call this function to trigger the updates
#     emit_room_temps()
#     return 'Updated'


# //// ROUTES \\\\ #
@app.route("/",methods=["GET","POST"])
def index(): 
    return redirect(url_for("homepage"))

@app.route("/homepage",methods=["GET","POST"])
def homepage(): 

    hvac_event.wait()  #  Make sure that HVAC instance is available before run this route 

    # Check if HVAC instance is available in the global simulation instance
    if "hvac" in simulation_instance:
        hvac_instance = simulation_instance["hvac"]
        room_temp = hvac_instance.get_room_temp()  # Retrieve room temperatures
        print(f"Room Temp from HVAC: {room_temp}")  # Debug print

        # Update the shared_data with room temperatures
        shared_data.update({
            "is_occupied": True,
            "room1_temperature": room_temp.get("Living Room", 10),
            "room2_temperature": room_temp.get("Bathroom", 12),
            "room3_temperature": room_temp.get("Bedroom", 14),
            "room4_temperature": room_temp.get("Kitchen", 16),
            "current_temperature": round((room_temp.get("Living Room", 10) + room_temp.get("Bathroom", 12) +
                                    room_temp.get("Bedroom", 14) + room_temp.get("Kitchen", 16)) / 4, 1),# Makes sure to round to 1 decimal place
            "is_HVAC_on": False,
            "HVAC_movement": 1
        })

    return render_template("homepage.html",
                           is_default_mode=is_default_mode,target_temperature=target_temperature,is_fire_alarm=is_fire_alarm,
                            is_occupied=shared_data["is_occupied"],
                            current_temperature=shared_data["current_temperature"],
                            is_HVAC_on=shared_data["is_HVAC_on"],
                            HVAC_movement=shared_data["HVAC_movement"])    


@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    hvac_event.wait()  #  Make sure that HVAC instance is available before run this route 

    # Check if HVAC instance is available in the global simulation instance
    if "hvac" in simulation_instance:
        hvac_instance = simulation_instance["hvac"]
        room_temp = hvac_instance.get_room_temp()  # Retrieve room temperatures
        print(f"Room Temp from HVAC: {room_temp}")  # Debug print

        # Update the shared_data with room temperatures dynamically
        shared_data.update({
            "is_occupied": True,
            "room1_temperature": room_temp.get("Living Room", 10),
            "room2_temperature": room_temp.get("Bathroom", 12),
            "room3_temperature": room_temp.get("Bedroom", 14),
            "room4_temperature": room_temp.get("Kitchen", 16),
            "current_temperature": round((room_temp.get("Living Room", 10) + room_temp.get("Bathroom", 12) +
                                    room_temp.get("Bedroom", 14) + room_temp.get("Kitchen", 16)) / 4, 1), # makes sure to always round it to 1 decimal place
            "is_HVAC_on": False,
            "HVAC_movement": 1
        })

        # Pass the correct room temperatures to the template
        return render_template("rooms.html",
                               current_temperature=shared_data["current_temperature"],
                               room1_temperature=shared_data["room1_temperature"],
                               room2_temperature=shared_data["room2_temperature"],
                               room3_temperature=shared_data["room3_temperature"],
                               room4_temperature=shared_data["room4_temperature"])
    else:
        return "No HVAC instance found." 


@app.route("/settings",methods=["GET","POST"])
def settings(): 

    return render_template("settings.html")   
