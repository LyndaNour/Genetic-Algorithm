from schedule import *
import random
import numpy as np
import copy

class Schedule:
    def __init__(self, activities):
        self.activities = activities

class ActivityAssignment:
    def __init__(self, activity, room, time, facilitator):
        self.activity = activity
        self.room = room
        self.time = time
        self.facilitator = facilitator

def initialize_schedule():
    activities = list(activities_data.keys())
    activity_assignments = []
    
    # Convert dict_keys object to list
    facilitator_keys = list(facilitators_data.keys())
    room_keys = list(room_capacity.keys())

    for activity in activities:
        room = random.choice(room_keys)
        time = random.choice(timeslots)
        facilitator = random.choice(facilitator_keys)
        activity_assignment = ActivityAssignment(activity, room, time, facilitator)
        activity_assignments.append(activity_assignment)
    schedule = Schedule(activity_assignments)
    return schedule

def initialize_population(population_size):
    population = []
    for i in range(population_size):
        schedule = initialize_schedule()
        population.append(schedule)
    return population

def calculate_fitness(schedule, room_capacity):
    fitness = 0
    
    # Create a dictionary to keep track of scheduled activities by time and room
    schedule_dict = {}
    facilitator_activities = {}
    
    # Iterate through each activity assignment in the schedule
    for activity_assignment in schedule.activities:
        # Create a key based on time and room for each activity assignment
        key = (activity_assignment.time, activity_assignment.room)
        schedule_dict.setdefault(key, []).append(activity_assignment)
        
        # Keep track of activities assigned to each facilitator
        facilitator = activity_assignment.facilitator
        facilitator_activities.setdefault(facilitator, []).append(activity_assignment)

    # Evaluate fitness based on scheduled activities in each time slot
    for activities_in_slot in schedule_dict.values():
        if len(activities_in_slot) > 1:
            # Penalize if more than one activity is scheduled in the same time slot
            fitness -= 0.5 * (len(activities_in_slot) - 1)
            
        for activity_assignment in activities_in_slot:
            facilitator = activity_assignment.facilitator
            expected_enrollment = activities_data[activity_assignment.activity]["Expected enrollment"]
            room_capacity_slot = room_capacity[activity_assignment.room]  # Get capacity of the room
            room_name = activity_assignment.room
            activity = activity_assignment.activity

            preferred_facilitators = activities_data[activity_assignment.activity].get("Preferred facilitators", [])
            other_facilitators = activities_data[activity].get("Other facilitators", [])
            
            # Check room size criteria for the slot
            if room_capacity_slot < expected_enrollment:
                fitness -= 0.5
            elif room_capacity_slot > 6 * expected_enrollment:
                fitness -= 0.4
            elif room_capacity_slot > 3 * expected_enrollment:
                fitness -= 0.2
            else:
                fitness += 0.3

            # Check if the assigned facilitator is preferred or other for the activity
            if facilitator in preferred_facilitators:
                fitness += 0.5
            elif facilitator in other_facilitators:
                fitness += 0.2
            else:
                fitness -= 0.1

    # Evaluate fitness based on facilitator constraints
    for facilitator, activities in facilitator_activities.items():
        assigned_times = set()  # To keep track of assigned times for each facilitator
        facilitator_activity_count = len(activities)
        
        for activity_assignment in activities:
            if activity_assignment.time in assigned_times:
                # Penalize if the facilitator is assigned to activities at the same time
                fitness -= 0.2  
            else:
                assigned_times.add(activity_assignment.time)
        
            # Check if facilitator is scheduled for only one activity in this time slot
            activities_in_slot = [a for a in activities if a.time == activity_assignment.time]
            if len(activities_in_slot) == 1:
                fitness += 0.2

            if len(activities) > 4:
                # Penalize if the facilitator is scheduled to oversee more than 4 activities total
                fitness -= 0.5
        
            # Apply penalty if the facilitator is overseeing only 1 or 2 activities
            if facilitator_activity_count <= 2 and facilitator != "Tyler":
                fitness -= 0.4
            # Exception for Dr. Tyler
            if facilitator == "Tyler" and facilitator_activity_count < 2:
                fitness += 0.4  # No penalty if Dr. Tyler is overseeing only 1 or 2 activities
                

    return fitness


#Normalization
def softmax(fitness_scores):
    e_x = np.exp(fitness_scores)
    return e_x / e_x.sum()

#Parents selection 
def select_parents(fitness_scores):
    probabilities = softmax(fitness_scores)
    parent_indices = np.random.choice(len(fitness_scores), size=2, p=probabilities)
    while parent_indices[0] == parent_indices[1]:  # Check if the indices are equal
        parent_indices = np.random.choice(len(fitness_scores), size=2, p=probabilities) 
    return parent_indices

#define offsprings 
def produce_offspring(parent1, parent2):
    offspring = copy.deepcopy(parent1)
    crossover_point = random.randint(0, len(parent1.activities) - 1)
    for i in range(crossover_point):
        offspring.activities[i] = parent2.activities[i]
    return offspring


def mutate_schedule(schedule, mutation_rate):
    mutated_activities = []
    random_number = random.random()
    for activity_assignment in schedule.activities:
        if random_number < mutation_rate:

            # Apply mutation to the activity assignment
            activity_assignment.activity = random.choice(list(activities_data.keys()))
            activity_assignment.room = random.choice(list(room_capacity.keys()))
            activity_assignment.time = random.choice(timeslots)
            activity_assignment.facilitator = random.choice(list(facilitators_data.keys()))

        mutated_activities.append(activity_assignment)
    mutated_schedule = Schedule(mutated_activities)
    return mutated_schedule




'''
def calculate_fitness(schedule, room_capacity):
    fitness = 0
    
    # Create a dictionary to keep track of scheduled activities by time and room
    schedule_dict = {}
    facilitator_activities = {}
    for activity_assignment in schedule.activities:
        key = (activity_assignment.time, activity_assignment.room)
        if key in schedule_dict:
            schedule_dict[key].append(activity_assignment)
        else:
            schedule_dict[key] = [activity_assignment]
        print("Key:", key)
        # Keep track of activities assigned to each facilitator
        facilitator = activity_assignment.facilitator
        if facilitator in facilitator_activities:
            facilitator_activities[facilitator].append(activity_assignment)
        else:
            facilitator_activities[facilitator] = [activity_assignment]

    for activities_in_slot in schedule_dict.values():
        for activity_assignment in activities_in_slot:
            if len(activities_in_slot) > 1:
                fitness -= 0.5 * (len(activities_in_slot) - 1)
                print("Conflict Detected: Room:", activity_assignment.room, "Time:", activity_assignment.time, "fitness:", fitness)
            
            facilitator = activity_assignment.facilitator
            expected_enrollment = activities_data[activity_assignment.activity]["Expected enrollment"]
            room_capacity_slot = room_capacity[activity_assignment.room]  # Get capacity of the room
            room_name = activity_assignment.room
            activity = activity_assignment.activity

            preferred_facilitators = activities_data[activity_assignment.activity].get("Preferred facilitators", [])
            other_facilitators = activities_data[activity].get("Other facilitators", [])
            facilitator = activity_assignment.facilitator

            # Check room size criteria for the slot
            if room_capacity_slot < expected_enrollment:
                fitness -= 0.5
                print("Room size is small:", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment,"facilitator:", facilitator, "fitness:", fitness )
            
            elif room_capacity_slot > 6 * expected_enrollment:
                fitness -= 0.4
                print("Room size is large (more than 6x):", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment, "facilitator:", facilitator, "fitness:", fitness )
                
            elif room_capacity_slot > 3 * expected_enrollment:
                fitness -= 0.2
                print("Room size is large (more than 3x):", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment, "facilitator:", facilitator, "fitness:", fitness )
                
            else:
                fitness += 0.3
                print("good room size, fitness add 0.3:", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment, "facilitator:", facilitator, "fitness:", fitness )

            # Check if the assigned facilitator is preferred or other for the activity
            if facilitator in preferred_facilitators:
                fitness += 0.5
                print("Room:", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment,"Assigned Facilitator:", facilitator, "Activity overseen by preferred facilitator:", facilitator, "fitness:", fitness)         
            elif facilitator in other_facilitators:
                fitness += 0.2
                print("Room:", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment,"Activity overseen by other facilitator:", facilitator, "fitness:", fitness)
            else:
                fitness -= 0.1
                print("Room:", room_name, "Capacity:", room_capacity_slot, "Activity:", activity, "Expected Enrollment:", expected_enrollment, "Activity overseen by some other facilitator:", facilitator, "fitness:", fitness)

            print("\n______________________________________Next activity________________________________\n")

            for i in range(len(activities_in_slot)):
                # Check if the current activity is SLA100A and the next activity is SLA100B
                if i < len(activities_in_slot) - 1:
                    next_activity = activities_in_slot[i + 1].activity
                    if activity == "SLA100A" and next_activity == "SLA100B":
                    # Perform actions for combining SLA100A and SLA100B activities
                        time_difference = abs(activity_assignment.time - activities_in_slot[i + 1].time)
                        if time_difference > 4:
                            fitness += 0.5
                            print("SLA 100 sections are more than 4 hours apart, adding 0.5 to fitness")
                        if time_difference ==0:
                            fitness -= 0.5
                            print("SLA 100 sections are scheduled in the same time, substract 0.5 to fitness")

                        else:
                            ("slas time is good")

    for facilitator, activities in facilitator_activities.items():
        assigned_times = set()  # To keep track of assigned times for each facilitator
        facilitator_activity_count = len(activities)
        for activity_assignment in activities:
            if activity_assignment.time in assigned_times:
             # Penalize if the facilitator is assigned to activities at the same time
                fitness -= 0.2  
                print("Facilitator", facilitator, "at time", activity_assignment.time, "assigned to multiple activities")
            else:
                assigned_times.add(activity_assignment.time)
        
            # Check if facilitator is scheduled for only one activity in this time slot
            activities_in_slot = [a for a in activities if a.time == activity_assignment.time]
            if len(activities_in_slot) == 1:
                fitness += 0.2
                print("At time", activity_assignment.time, "Facilitator", facilitator," is assigned to one activity")


            if len(activities) > 4:
            # Penalize if the facilitator is scheduled to oversee more than 4 activities total
                fitness -= 0.5
                print("Facilitator", facilitator, "is scheduled to oversee more than 4 activities total")
        
       # Apply penalty if the facilitator is overseeing only 1 or 2 activities
        if facilitator_activity_count <= 2 and facilitator !="Tyler":
            fitness -= 0.4
            print(f"Facilitator {facilitator} is overseeing {facilitator_activity_count} activities, penalizing fitness.")
        # Exception for Dr. Tyler
        if facilitator == "Tyler" and facilitator_activity_count < 2:
            fitness += 0.4  # No penalty if Dr. Tyler is overseeing only 1 or 2 activities
            print("Dr. Tyler has exception, no penalty.")

    return fitness

    
def calculate_fitness(schedule, room_capacity):
    fitness = 0
    
    # Create a dictionary to keep track of scheduled activities by time and room
    schedule_dict = {}
    facilitator_activities = {}
    
    for activity_assignment in schedule.activities:
        key = (activity_assignment.time, activity_assignment.room)
        schedule_dict.setdefault(key, []).append(activity_assignment)
        
        # Keep track of activities assigned to each facilitator
        facilitator = activity_assignment.facilitator
        facilitator_activities.setdefault(facilitator, []).append(activity_assignment)

    for activities_in_slot in schedule_dict.values():
        if len(activities_in_slot) > 1:
            fitness -= 0.5 * (len(activities_in_slot) - 1)
            
        for activity_assignment in activities_in_slot:
            facilitator = activity_assignment.facilitator
            expected_enrollment = activities_data[activity_assignment.activity]["Expected enrollment"]
            room_capacity_slot = room_capacity[activity_assignment.room]  # Get capacity of the room
            room_name = activity_assignment.room
            activity = activity_assignment.activity

            preferred_facilitators = activities_data[activity_assignment.activity].get("Preferred facilitators", [])
            other_facilitators = activities_data[activity].get("Other facilitators", [])
            
            # Check room size criteria for the slot
            if room_capacity_slot < expected_enrollment:
                fitness -= 0.5
            elif room_capacity_slot > 6 * expected_enrollment:
                fitness -= 0.4
            elif room_capacity_slot > 3 * expected_enrollment:
                fitness -= 0.2
            else:
                fitness += 0.3

            # Check if the assigned facilitator is preferred or other for the activity
            if facilitator in preferred_facilitators:
                fitness += 0.5
            elif facilitator in other_facilitators:
                fitness += 0.2
            else:
                fitness -= 0.1

    for facilitator, activities in facilitator_activities.items():
        assigned_times = set()  # To keep track of assigned times for each facilitator
        facilitator_activity_count = len(activities)
        
        for activity_assignment in activities:
            if activity_assignment.time in assigned_times:
                # Penalize if the facilitator is assigned to activities at the same time
                fitness -= 0.2  
            else:
                assigned_times.add(activity_assignment.time)
        
            # Check if facilitator is scheduled for only one activity in this time slot
            activities_in_slot = [a for a in activities if a.time == activity_assignment.time]
            if len(activities_in_slot) == 1:
                fitness += 0.2

            if len(activities) > 4:
                # Penalize if the facilitator is scheduled to oversee more than 4 activities total
                fitness -= 0.5
        
            # Apply penalty if the facilitator is overseeing only 1 or 2 activities
            if facilitator_activity_count <= 2 and facilitator != "Tyler":
                fitness -= 0.4
            # Exception for Dr. Tyler
            if facilitator == "Tyler" and facilitator_activity_count < 2:
                fitness += 0.4  # No penalty if Dr. Tyler is overseeing only 1 or 2 activities
                

    return fitness

    '''

