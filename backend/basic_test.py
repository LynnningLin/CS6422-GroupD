import simpy.rt
from random import seed, randint, choice
from datetime import datetime
import json
from ANSI import Colours # Module used to style terminal using ANSI cdoes

# :TODO Make separate channels for both Temp and Motion sensors
radio_channel = 0

debug_radio = False
debug_sensor = True
"""
test
"""

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
        print(f'{Colours.GREEN}{self.env.now} : {self.UUID} : {self.node_type} : HVAC Online {Colours.RESET}')

    def main_process(self):
        while True:
            yield self.env.timeout(100) #  HVAC will broadcasting "Waiting for data" until receives data
            print(self.env.now, ":", f'{Colours.CYAN}{self.UUID}{Colours.RESET}' " HVAC waiting for data")

    def receive_process(self):
        while True:
            message = yield self.data_in.get()
            data_string = self.receive_data(message)
            if data_string:
                print(f'{Colours.MAGENTA}{self.env.now} : {Colours.RESET}{Colours.CYAN}{self.UUID}{Colours.RESET}{Colours.MAGENTA} HVAC receiving {data_string}{Colours.RESET}')


# //// SENSORS \\\\ #
class TemperatureSensor(Node):
    def __init__(self, env, medium, room_name, node_type, UUID): # Initialises new sensor object that inherits from Node
        super().__init__(env, medium, room_name, node_type, UUID) # Accessing Parent class(Node) method and properties
        print(f'{Colours.GREEN}{self.env.now} : {self.UUID} : {self.node_type} : {self.room_name} :  New Temp-Sensor Online {Colours.RESET}')

    def temperature(self):
        temp = randint(27, 35)
        if debug_sensor:
            print(self.env.now, ":", f'{Colours.YELLOW}{self.UUID}{Colours.RESET}', "Reading temps of:", temp,"°C")
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
            print(f'{Colours.MAGENTA}{self.env.now} : {Colours.RESET}{Colours.YELLOW}{self.UUID}{Colours.RESET}{Colours.MAGENTA} sending {string_data}{Colours.RESET}')
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
        print(f'{Colours.GREEN}{self.env.now} : {self.UUID} : {self.node_type} : {self.room_name} :  New Motion-Sensor Online {Colours.RESET}')

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
                    print(self.env.now, ":", f'{Colours.RED}{self.UUID}{Colours.RESET}', "Status changed: Someone is Home") # Change Status
                else: 
                    print(self.env.now, ":", f'{Colours.RED}{self.UUID}{Colours.RESET}', "Status changed: Nobody is Home")

                print(f'{Colours.MAGENTA}{self.env.now} : {Colours.RESET}{Colours.RED}{self.UUID}{Colours.RESET}{Colours.MAGENTA} sending {string_data}{Colours.RESET}')
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

# env = simpy.rt.RealtimeEnvironment(factor=0.01)
env = simpy.rt.RealtimeEnvironment(factor=0.01, strict=False) # set "strict" to False, now simulation can be "too slow" without throwing errors
medium = Medium(env)

HVAC(env, medium, 'Actuator', 'A001')

TemperatureSensor(env, medium, 'Living Room', 'T-Sensor', 'TS001')
TemperatureSensor(env, medium, 'Bathroom', 'T-Sensor', 'TS002')
TemperatureSensor(env, medium, 'Bedroom', 'T-Sensor', 'TS003')
TemperatureSensor(env, medium, 'Kitchen', 'T-Sensor', 'TS004')

MotionSensor(env, medium, 'Home', 'M-Sensor', 'MS001')

env.run(until=6000)
