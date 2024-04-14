import numpy as np
from randomSchedule import *
from schedule import *


def main():
    population_size = 10  # Adjust the population size as needed
    mutation_rate = 0.01
    max_generations = 120

    population = genetic_algorithm(population_size, mutation_rate, max_generations)



    print_population(population)

def print_population(population):
    for idx, schedule in enumerate(population):
        print(f"Schedule {idx + 1}:")
        for assignment in schedule.activities:
            print(f"Activity: {assignment.activity}, Room: {assignment.room}, Time: {assignment.time}, Facilitator: {assignment.facilitator}")
        print("\n")

def genetic_algorithm(population_size, mutation_rate, max_generations):
    population = initialize_population(population_size)
    prev_avg_fitness = float('inf')  # Initialize with a large value to ensure the loop starts
 
    
    for generation in range(1, max_generations + 1):

        fitness_scores = [calculate_fitness(schedule, room_capacity) for schedule in population]
        softmax(fitness_scores)
        
        avg_fitness = round(sum(fitness_scores) / len(fitness_scores),2)
        rounded_scores = [round(score, 2) for score in fitness_scores]
        print("generation:", generation, "List of scores",rounded_scores, "average:", round(avg_fitness,2))
        
        # Check if improvement falls below threshold
        if generation > 100 and (prev_avg_fitness - avg_fitness) / prev_avg_fitness < 0.01:
            print(f"Improvement in average fitness falls below 1% after generation {generation}. Stopping...")
            break
        
        # Update prev_avg_fitness for next iteration
        prev_avg_fitness = avg_fitness
        best_fitness = round(max(fitness_scores),2)
        print("best fitness", best_fitness)

        next_generation = []
        for _ in range(population_size):  # Produce offspring for entire population
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            offspring = produce_offspring(parent1, parent2)
            offspring_mutation = mutate_schedule(offspring, mutation_rate)
            next_generation.append(offspring_mutation)
        
        population = next_generation

        # Print the final schedule
    print("\nFinal Schedule:")
    best_schedule = max(population, key=lambda schedule: calculate_fitness(schedule, room_capacity))
    best_fitness = calculate_fitness(best_schedule, room_capacity)

     # Write the best schedule to an output file
    output_file_path = "best_schedule.txt"
    with open(output_file_path, "w") as output_file:
        output_file.write("Best Schedule:\n")
        for assignment in best_schedule.activities:
            output_file.write(f"Activity: {assignment.activity}, Room: {assignment.room}, "
                              f"Time: {assignment.time}, Facilitator: {assignment.facilitator}\n")
            
    print(f"Best schedule written to {output_file_path}")

    print("Best fitness", best_fitness, "generation:", generation)
    for assignment in best_schedule.activities:
        print(f"Activity: {assignment.activity}, Room: {assignment.room}, Time: {assignment.time}, Facilitator: {assignment.facilitator}")
    
    return population

if __name__ == "__main__":
    main()
