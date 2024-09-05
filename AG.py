import networkx as nx
import random

# Integrantes da dupla: Nicolas Teles e Miguel de Assis

POPULATION_SIZE = 150
ELITE_PERCENTAGE = 0.5
NUMBER_OF_GENERATIONS = 500
MUTATION_CHANCE = 0.1


def generate_population(graph: nx.Graph, population_size: int) -> list[list[int]]:
    nodes = list(graph.nodes())
    population = []
    for i in range(population_size):
        individual = random.sample(nodes, len(nodes))  # Permutação dos nós
        individual.append(individual[0])  # Retornar ao ponto inicial
        population.append(individual)
    return population
            
def mutate(individual: list[int]) -> list[int]:
    if random.random() > MUTATION_CHANCE:
        return individual
    # Trocar dois nós
    index1, index2 = random.sample(range(0, len(individual)-1), 2)
    individual[index1], individual[index2] = individual[index2], individual[index1]
    individual[-1] = individual[0]
    return individual

def fitnessFuction(graph: nx.Graph, individual: list[int]) -> int:
    custo = 0
    for i in range(len(individual)-1):
        node1 = individual[i]
        node2 = individual[i+1]
        
        custo += graph[node1][node2]['peso']
    
    return custo

def elitismo(population: list[list[int]], fitness_dict: dict) -> list[list[int]]:
    numSelecionados = int(POPULATION_SIZE * ELITE_PERCENTAGE)
    elite = sorted(population, key=lambda ind: fitness_dict[tuple(ind)])[:numSelecionados]
    return elite

def select_parents(elite: list[list[int]], fitness_dict: dict) -> list[list[int]]:
    fitness_list = [fitness_dict[tuple(individual)] for individual in elite]
    total_fitness = sum(fitness_list)
    probabilities = [fitness / total_fitness for fitness in fitness_list]
    return random.choices(elite, probabilities, k=2)

def crossover(elite: list[list[int]], fitness_dict: dict) -> list[int]:
    parents = select_parents(elite, fitness_dict)
    size = len(parents[0]) - 1
    child = [None] * size

    # Definir um segmento do primeiro pai
    start, end = sorted([random.randint(0, size-1) for _ in range(2)])
    child[start:end] = parents[0][start:end]

    # Preencher o restante com o segundo pai
    pos = end
    for node in parents[1]:
        if node not in child:
            if pos >= size:
                pos = 0
            child[pos] = node
            pos += 1

    child.append(child[0])  # Fechar ciclo
    return child

def main():   
    grafo: nx.Graph = nx.read_gml('PCV.gml')
    populacao = generate_population(grafo, POPULATION_SIZE)
    
    fitness_dict = {}
    for individual in populacao:
        fitness_dict[tuple(individual)] = fitnessFuction(grafo, individual)
    
    for _ in range(NUMBER_OF_GENERATIONS):
        elite = elitismo(populacao, fitness_dict)
        
        # Atualizar dicionário de fitness
        new_population = elite[:]
        
        while len(new_population) < POPULATION_SIZE:
            new_individual = mutate(crossover(elite, fitness_dict))
            fitness_dict[tuple(new_individual)] = fitnessFuction(grafo, new_individual)
            new_population.append(new_individual)
        populacao = new_population
    sorted_population = sorted(populacao, key=lambda individual: fitness_dict[tuple(individual)])
    best_individual = sorted_population[0]

    lista_fitness = [fitness_dict[tuple(ind)] for ind in sorted_population]
    
    # print(f"População final: {sorted_population}")
    # print(lista_fitness)
    best_fitness = lista_fitness[0]
    print(f"Melhor rota: {best_individual}")
    print(f"Custo da melhor rota: {best_fitness}")

main()