# python3.10 -m flask run
from flask import Flask,render_template,url_for,redirect,request
# from forms import SettingsForm
import random
# from datetime import datetime,date
import threading
import queue
import time
from forms import settingsForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-my-secret-key"

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

# system configuration for setting page
system_config = {
    'target_temperature': 25,
    'occupation_detect': False,
    'fire_alarm': False,
    'mode': 'Default Mode'
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
    # initialize target temperature
    target_temperature = 25
    system_config['mode'] = 'default'
    if request.method == 'POST':
        # Handle the form submission from /settings
        mode = request.form.get('mode')  
        target_temperature = request.form.get('target_temperature')
        occupation_detect = request.form.get('occupation_detect') == 'on'  
        fire_alarm = request.form.get('fire_alarm') == 'on' 
        
        # I dont know why print doesn't work in flask :(
        print(f"Mode updated to: {mode}")
        print(f"Target Temperature: {target_temperature}")
        print(f"Occupation Detect: {occupation_detect}")
        print(f"Fire Alarm: {fire_alarm}")
       
        
        
        system_config['mode'] = mode
        system_config['target_temperature'] = target_temperature
        system_config['occupation_detect'] = occupation_detect
        system_config['fire_alarm'] = fire_alarm
        
        print(f"Mode updated to: {system_config['mode']}") 
        
    shared_data["room1_temperature"] = random.randint(10, 40)
    shared_data["room2_temperature"] = random.randint(10, 40)
    shared_data["room3_temperature"] = random.randint(10, 40)
    shared_data["room4_temperature"] = random.randint(10, 40)
    
    shared_data["current_temperature"] = int((shared_data["room1_temperature"]+shared_data["room2_temperature"]+shared_data["room3_temperature"]+shared_data["room4_temperature"])/4)    
    
    return render_template("homepage.html",
                           system_config=system_config,
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
    print("Inside settings route")

    form = settingsForm()
    if form.validate_on_submit():
        print("Form submitted") 
        system_config['target_temperature'] = form.target_temperature.data
        system_config['occupation_detect'] = form.occupation_detect.data
        system_config['fire_alarm'] = form.fire_alarm.data
        system_config['mode'] = form.mode.data
        
        return redirect(url_for('homepage')) 


    return render_template("settings.html", form=form, system_config=system_config)   

if __name__ == '__main__':
    app.run(debug=True)
