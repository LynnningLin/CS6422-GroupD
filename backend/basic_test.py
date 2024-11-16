import simpy.rt
from random import seed, randint, choice
from datetime import datetime
import json
import queue
import threading
import time




""" 
This is a placeholder for when I try to attempt importing ANSI again,   
it's just clashing with flask so i disabled it for the time being
"""
# try:
#         from ANSI import Colours  # Import only for terminal output
#         print(("Simulation in progress..."))
# except ImportError:
#         print("Simulation in progress... (no terminal styling)")


# :TODO Make separate channels for both Temp and Motion sensors
radio_channel = 0

debug_radio = False
debug_sensor = True

input_queue = queue.Queue()

class Medium(object): # medium == wireless channel to communicate
    def __init__(self, env, capacity=simpy.core.Infinity):
        """
        -env == declaring the simpy environment

        -capacity == capacity of the mediums on transmissions --> set to infinity for ease of use

        -communication_link_list == list of connection/communication links that are stored when connections are made during the simulation
        """

        self.env = env
        self.capacity = capacity
        self.communication_link_list = []

    def transmit(self, data): # sending data through medium

        """
        -If there are no available connections/communication links --> raise a runtime error

        -else it will loop through the communication_links in the list and transmit data 
        """

        if not self.communication_link_list:
            raise RuntimeError("There are no output connections available")
        events = []
        for store in self.communication_link_list:
            events.append(store.put(data))

    def get_output_connections(self, uuid=None):
        communication_link = simpy.Store(self.env, capacity=self.capacity) # create a new comm link
        communication_link.uuid = uuid
        self.communication_link_list.append(communication_link) # comm added to list of comm links
        return communication_link # return the communication link

# //// PARENT CLASS FOR SENSROS/ACTUATORS \\\\ #
class Node(object): # Basic Node class that both HVACC Actuator AND Temp/Motion sensors will inherit from
    def __init__(self, env, medium, room_name, node_type, UUID):
        self.env = env
        self.data_in = medium.get_output_connections()   # Nodes get data in
        # self.data_in = medium.get_output_connections(uuid = self.UUID) # First fix attempt, did not work, will probably remove
        self.data_out = medium  # Nodes send data out 
        self.room_name = room_name 
        self.channel = radio_channel
        self.UUID = UUID # Unique identifier for every node, regardless of type/room
        self.node_type = node_type # What type of Sensor is it --> Temp/Motion etc
        # self.message_log = 0 Might get rid of this, wanted to log all messages sent between sensors don't think it's necessayr
        env.process(self.main_process())
        env.process(self.receive_process())

    def send_data(self, destination, string_data): # Method to create and send out data
        if debug_radio:  # If debug_radio is true
            print(self.UUID, self.env.now, ":", self.room_name, ":", self.node_type, "-->", destination)  # Print the realtime ,Node/Id_header, destination location and data payload
        
        message = (self.UUID, self.room_name, self.node_type, destination, str(string_data)) 
        # self.data_out.put(message) # actually sends the message using data_out
        self.data_out.transmit(message) # Changed so that the message is sent directly using "transmit"
        # IMPORTANT: Moved the preceding lines out of "if debug_radio", which we still have set to False

    def receive_data(self, message):  # Method to receive and handle incoming data
        if message[3] == self.UUID: # Check if message was intended for this node using UUID, [3] is destination in the message tuple on line 66
            if debug_radio:
                print(self.env.now, ":", self.UUID, "<--")
            return str(message[4])
        if debug_radio:
            print(self.env.now, ":", self.UUID, "X")
        return None

# //// ACTUATORS \\\\ #
class HVAC(Node):
    def __init__(self, env, medium, node_type, UUID):
        super().__init__(env, medium, None, node_type, UUID)
        print(f'{self.env.now} : {self.UUID} : {self.node_type} : HVAC Online')

        # print(f'{Colours.GREEN}{self.env.now} : {self.UUID} : {self.node_type} : HVAC Online {Colours.RESET}')


        self.target_temperature = 22 # HVAC stores the target temperature for now
        self.occupied = True # Occupancy status of house

        self.room_temperatures = { # This is a dictionary where we store the current temp. for each room, makes it easier/cleaner to iterate through and update them
            "Living Room": self.target_temperature,
            "Bathroom": self.target_temperature,
            "Bedroom": self.target_temperature,
            "Kitchen": self.target_temperature
            }
    
    def get_room_temp(self):
        return self.room_temperatures

    def main_process(self):
        while True:
            yield self.env.timeout(100)

            try: # First we check the input queue to see whether target temperature has been updated
                self.target_temperature = input_queue.get_nowait()
                print(f"Thermostat received new target: {self.target_temperature}")
            except queue.Empty:
                    pass
            
            if self.occupied: # We then check occupancy status. If someone is home, we update the temperature as per usual
                for room, temperature in self.room_temperatures.items():
                    if temperature < self.target_temperature:
                        # print(self.env.now, ":", f'{Colours.CYAN}{self.UUID}{Colours.RESET}' " Current " f'{Colours.GREEN}{room}{Colours.RESET}' " temp is " f'{Colours.BLUE}{temperature}{Colours.RESET}' ", increasing" )
                        print(self.env.now, ":", f'{self.UUID}' " Current " f'{room}' " temp is " f'{temperature}' ", increasing" )
                        self.room_temperatures[room] = temperature+1
                        # print(f'{room} {temperature} Data display test ') This was just some minor debugging

                    elif temperature > self.target_temperature:
                        # print(self.env.now, ":", f'{Colours.CYAN}{self.UUID}{Colours.RESET}' " Current " f'{Colours.GREEN}{room}{Colours.RESET}' " temp is " f'{Colours.RED}{temperature}{Colours.RESET}' ", decreasing" )
                        print(self.env.now, ":", f'{self.UUID}' " Current " f'{room}' " temp is " f'{temperature}' ", decreasing" )
                        self.room_temperatures[room] = temperature-1

            # yield self.env.timeout(100) #  HVAC will broadcasting "Waiting for data" until receives data
            # print(self.env.now, ":", f'{self.UUID}' " HVAC waiting for data")

    def receive_process(self):
        while True:
            message = yield self.data_in.get()
            data_string = self.receive_data(message)
            if data_string:
                print(f'{self.env.now} : {self.UUID} HVAC receiving {data_string}')

            data_reading = json.loads(data_string)
                
            room_reading = data_reading.get('Room')

            if room_reading != 'Home': # If the reading is for one of our rooms, we set the temp. to that room to the new current temp.
                self.room_temperatures[room_reading] = data_reading.get('DATA')
            else: # Otherwise the reading is for our occupancy status, which we also update
                self.occupied = data_reading.get('IsOccupied')


# //// SENSORS \\\\ #
class TemperatureSensor(Node):
    def __init__(self, env, medium, room_name, node_type, UUID): # Initialises new sensor object that inherits from Node
        super().__init__(env, medium, room_name, node_type, UUID) # Accessing Parent class(Node) method and properties
        print(f'{self.env.now} : {self.UUID} : {self.node_type} : {self.room_name} :  New Temp-Sensor Online ')

    def temperature(self):
        temp = randint(27, 35)
        if debug_sensor:
            print(self.env.now, ":", f'{self.UUID}', "Reading temps of:", temp,"°C")
        return temp

    def main_process(self):
        while True:
            yield self.env.timeout(randint(500, 1000))
            # self.message_log += 1

            json_message = {}
            json_message['UUID'] = self.UUID
            # json_message['Message-Log'] = self.message_log
            json_message['Room'] = self.room_name
            json_message['Type'] = self.node_type
            json_message['Destination'] = 'A001' 
            json_message['DATA'] = self.temperature()
            string_data = json.dumps(json_message)
            print(f'{self.env.now} : {self.UUID} sending {string_data}')
            self.send_data(json_message['Destination'], string_data)  
    
    def receive_process(self):
        while True:
            message = yield self.data_in.get()
            data_string = self.receive_data(message)
            if data_string:
                print(self.env.now,':', self.UUID ,' receiving ' , data_string)


class MotionSensor(Node):

    """

    Motion sensor works similar to Temp sensor in inhreitance/sending data 

    Differences:
        -Motion Sensor only detects the change whether isOccupied to True or False
        -It won't log redundant statuses --> Only changes in status
        -Message/Data will also only send if there is a status change, decluttering the logs in the terminal

    """

    def __init__(self, env, medium, room_name, node_type, UUID): # Initialises new sensor object that inherits from Node
        super().__init__(env, medium, room_name, node_type, UUID) # Accessing Parent class(Node) method and properties
        print(f'{self.env.now} : {self.UUID} : {self.node_type} : {self.room_name} :  New Motion-Sensor Online ')

    def occupancy(self): # Occupancy Check whether T/F
        isOccupied = choice([True, False]) # Stored Possible Values
        return isOccupied

    def main_process(self):
        previous_status = None # Stores last known Occupancy Status --> Status Dump

        while True:
            occupancy_status = self.occupancy() # Gets current occupancy status 

            if occupancy_status != previous_status: # if status has changed from the previous status
                previous_status = occupancy_status # Updates previous occupancy status

                # self.message_log += 1
                json_message = {}
                json_message['UUID'] = self.UUID
                # json_message['Message-Log'] = self.message_log
                json_message['Room'] = self.room_name
                json_message['Type'] = self.node_type
                json_message['Destination'] = 'A001' 
                json_message["IsOccupied"] = occupancy_status
                string_data = json.dumps(json_message)

            # Print status change
                if occupancy_status: # If occupancy status is True
                    print(self.env.now, ":", f'{self.UUID}', "Status changed: Someone is Home") # Change Status
                else: 
                    print(self.env.now, ":", f'{self.UUID}', "Status changed: Nobody is Home")

                print(f'{self.env.now} : {self.UUID} sending {string_data}')
                self.send_data(json_message['Destination'], string_data) # Will only send data if there is a change in Occupancy Status

                yield self.env.timeout(randint(1000, 3000)) 
                
    def receive_process(self):
        while True:
            message = yield self.data_in.get()
            data_string = self.receive_data(message)
            if data_string:
                print(self.env.now,':', self.UUID ,' receiving ' , data_string)


# //// EANVIRONMENT \\\\ #

# Start of main program
seed(int(datetime.now().timestamp()))
"""
A huge chunk of the Environment i swapped out sadly,
I put the simpy env.run/realtime/medium with all the declared instances in the flask app.py so it would be directly from flask,
i would still like to have the backend side user input that Eighan made as i think it would be very cool for a hypothical backend/maintnence user to be able to use,
Maybe if__name__ == "main" we could give backend user input if the script is being directly ran rather than through the app.py script
I know this is tehcnically already happening but I'm just not sure what the target for the simulation_thread would be if 
I took the classes out of the simulation function 

"""

# env = simpy.rt.RealtimeEnvironment(factor=0.01)
# env = simpy.rt.RealtimeEnvironment(factor=0.01, strict=False) # set "strict" to False, now simulation can be "too slow" without throwing errors
# medium = Medium(env)

# HVAC(env, medium, 'Actuator', 'A001')

# TemperatureSensor(env, medium, 'Living Room', 'T-Sensor', 'TS001')
# TemperatureSensor(env, medium, 'Bathroom', 'T-Sensor', 'TS002')
# TemperatureSensor(env, medium, 'Bedroom', 'T-Sensor', 'TS003')
# TemperatureSensor(env, medium, 'Kitchen', 'T-Sensor', 'TS004')

# MotionSensor(env, medium, 'Home', 'M-Sensor', 'MS001')

# env.run(until=6000)


# def user_input(input_queue): # Completely separate function for handling user input
#     while True:
#         user_input = input() # This works but needs improving, user input gets swallowed by the terminal readouts (i.e.: visual issue) 
#         try:
#             target_temperature = int(user_input)
#             input_queue.put(target_temperature)
#             print(f"Temperature set to {target_temperature}")
#         except ValueError:
#             print("Please enter a valid number.")

# # //// MAIN \\\\ #
# if __name__ == "__main__":
#     input_queue = queue.Queue() # Queue allows us to send information between threads
#     input_thread = threading.Thread(target=user_input, args=(input_queue,))
#     simulation_thread = threading.Thread(target=env, args=(input_queue,))

#     input_thread.daemon = True  # Ensures that we exit even if one program keeps going after interrupt
#     simulation_thread.daemon = True

#     input_thread.start()
#     simulation_thread.start()

#     try:
#         while True:
#             time.sleep(0.1) # Briefly pauses main thread after each loop
#     except KeyboardInterrupt:
#         print("\nSimulation stopped.")