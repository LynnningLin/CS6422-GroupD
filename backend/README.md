# Basic Logic for Sensors/Actuators

## Log
* Very bareboned script for sensors and actuators
* Experienced problems with data transmission, data is sent but HVAC is having problems with receiving
* Didn't impliment all logic but the classes are all set up and other classes/Methods would be simple enough to add, Just the basic foundation was a little tricky
<hr>


### Nodes Intended Logic
* Base Node where both the Actuators(HVAC) and Sensors will inherit from
* Both HVAC and Sensor start up on run
* HVAC waits for data
* Random temperature readings create for simulation
* Sensors detect temp 
* Send data to HVAC

### Bugs
* Small bug with HVAC --> Sensors send data to HVAC but HVAC never receives data --> More than likely a medium transmission problem or a problem with the json message payload, I'm pretty sure it's the destination and UUID not matching. Will fix ASAP
<hr>

### Motion Sensor Class
* Below the TemperatureSensors class is a commented block of code
* This is just a WIP for the motion sensor
* Will inherit mostly the same attributes as TemperatureSensor
* Only difference is the Boolean --> isOccupied = True/False
<hr>

### ANSI Module
* I am using ANSI escape codes to style the terminal
* Most Print statements in the main script use the ANSI colours
* The class Colours is just for now
* I'm hoping to add more styling options to the terminal and will use the exisitng Colours class to style more

