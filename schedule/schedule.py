
import random

# Define classes
class Facilitator:
    def __init__(self, name, preferred_activities=None, other_activities=None):
        self.name = name
        self.preferred_activities = preferred_activities or [] # if not provided, it defaults to empty list 
        self.other_activities = other_activities or []

class Activity:
    def __init__(self, name, expected_enrollment, preferred_facilitators=None, other_facilitators=None):
        self.name = name,
        self.expected_enrollment = expected_enrollment
        self.preferred_facilitators = preferred_facilitators or []
        self.other_facilitators = other_facilitators or []

class Room: 
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

# Initialize data
facilitators_data = {
    "Lock": ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA291"],
    "Glen": ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA303", "SLA304"],
    "Banks": ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304", "SLA451"],
    "Richards": ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA304", "SLA394", "SLA451"],
    "Shaw": ["SLA201", "SLA291", "SLA303", "SLA304", "SLA449", "SLA451"],
    "Singer": ["SLA201", "SLA291", "SLA303", "SLA304", "SLA394", "SLA449", "SLA451"],
    "Uther": ["SLA304", "SLA449", "SLA451"],
    "Tyler": ["SLA304", "SLA394", "SLA449", "SLA451"],
    "Numen": ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304"],
    "Zeldin": ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304", "SLA394", "SLA449", "SLA451"]
}

activities_data = {
    "SLA100A": {
        "Expected enrollment": 50, 
        "Preferred facilitators": ["Glen", "Lock", "Banks", "Zeldin"], 
        "Other facilitators": ["Numen", "Richards"]
        },
    "SLA100B": {
        "Expected enrollment": 50, 
        "Preferred facilitators": ["Glen", "Lock", "Banks", "Zeldin"], 
        "Other facilitators": ["Numen", "Richards"]},
    "SLA191A": {
        "Expected enrollment": 50,
        "Preferred facilitators": ["Glen", "Lock", "Banks", "Zeldin"],
        "Other facilitators": ["Numen", "Richards"]
    },
    "SLA191B": {
        "Expected enrollment": 50,
        "Preferred facilitators": ["Glen", "Lock", "Banks", "Zeldin"],
        "Other facilitators": ["Numen", "Richards"]
    },
    "SLA201": {
        "Expected enrollment": 50,
        "Preferred facilitators": ["Glen", "Banks", "Zeldin", "Shaw"],
        "Other facilitators": ["Numen", "Richards", "Singer"]
    },
    "SLA291": {
        "Expected enrollment": 50,
        "Preferred facilitators": ["Lock", "Banks", "Zeldin", "Singer"],
        "Other facilitators": ["Numen", "Richards", "Shaw", "Tyler"]
    },
    "SLA303": {
        "Expected enrollment": 60,
        "Preferred facilitators": ["Glen", "Zeldin", "Banks"],
        "Other facilitators": ["Numen", "Singer", "Shaw"]
    },
    "SLA304": {
        "Expected enrollment": 25,
        "Preferred facilitators": ["Glen", "Banks", "Tyler"],
        "Other facilitators": ["Zeldin", "Numen", "Singer", "Shaw", "Richards", "Uther"]
    },
    "SLA394": {
        "Expected enrollment": 20,
        "Preferred facilitators": ["Tyler", "Singer"],
        "Other facilitators": ["Richards", "Zeldin"]
    },
    "SLA449": {
        "Expected enrollment": 60,
        "Preferred facilitators": ["Tyler", "Singer", "Shaw"],
        "Other facilitators": ["Zeldin", "Uther"]
    },
    "SLA451": {
        "Expected enrollment": 100,
        "Preferred facilitators": ["Tyler", "Singer", "Shaw"],
        "Other facilitators": ["Zeldin", "Uther", "Richards", "Banks"]
    }
}

room_capacity = {
    "Slater 003": 45,
    "Roman 216": 30,
    "Loft 206": 75,
    "Roman 201": 50,
    "Loft 310": 108,
    "Beach 201": 60,
    "Beach 301": 75,
    "Logos 325": 450,
    "Frank 119": 60
}

timeslots = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

# Function to create facilitator instances
def create_facilitators():
    facilitators = {}
    for facilitator_name, activity_list in facilitators_data.items():
        facilitator = Facilitator(facilitator_name)
        for activity_name in activity_list:
            if activity_name in activities_data:
                activity_info = activities_data[activity_name]
                preferred_facilitators = activity_info.get("Preferred facilitators", [])
                other_facilitators = activity_info.get("Other facilitators", [])
                if facilitator_name in preferred_facilitators:
                    facilitator.preferred_activities.append(activity_name)
                elif facilitator_name in other_facilitators:
                    facilitator.other_activities.append(activity_name)
        facilitators[facilitator_name] = facilitator
    return facilitators

# Function to create activity instances
def create_activities():
    activities = {}
    for activity_name, info in activities_data.items():
        expected_enrollment = info.get("Expected enrollment", 0)  # Default to 0 if key is missing
        preferred_facilitators = info.get("Preferred facilitators", [])
        other_facilitators = info.get("Other facilitators", [])
        activities[activity_name] = Activity(activity_name, expected_enrollment, preferred_facilitators, other_facilitators)
    return activities

# Function to create room instances
def create_rooms():
    rooms = {}
    for room_name, capacity in room_capacity.items():  
        rooms[room_name] = Room(room_name, capacity)
    return rooms


