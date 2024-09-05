import networkx as nx
import matplotlib.pyplot as plt
import random

POPULATION_SIZE = 10
ELITE_PERCENTAGE = 0.5


def generate_population(graph: nx.Graph, population_size: int) -> list[list[int]]:
    population = []
    
    for i in range(population_size):
        population.append([])
        while len(population[i]) < graph.number_of_nodes():
            random_num = random.randint(1, 5)
            if(random_num in population[i]):
                continue
            population[i].append(random_num)
        population[i].append(population[i][0])
    #print(population)
    return population
            

def mutate(graph: nx.Graph, individual: list[int]) -> list[int]:
    if(random.random() > 0.07):
        return individual
    index1 = random.randint(0, len(individual)-1)
    index2 = random.randint(0, len(individual)-1)
    new_individual = [city for city in individual]
    new_individual[index1], new_individual[index2] = new_individual[index2], new_individual[index1]
    new_individual[-1] = new_individual[0]
    return new_individual
    

def fitnessFuction(graph: nx.Graph, individual: list[int]) -> int:
    custo = 0
    for i in range(len(individual)-1):
        node1 = individual[i]
        node2 = individual[i+1]
        # print(f"no1: {node1}\nno2: {node2}")
        if graph.has_edge(node1, node2):
            custo += graph[node1][node2]['peso']
    return custo

def select_parents(graph: nx.Graph, elite: list[list[int]]) -> list[list[int]]:
    fitness_list = [fitnessFuction(graph, individual) for individual in elite]
    total_fitness = sum(fitness_list)
    lista_aptidao = [fitness/total_fitness for fitness in fitness_list]
    parents_list = []
    break_flag = False
    while True:
        for i in range(len(lista_aptidao)):
            random_chance = random.random()
            if random_chance > lista_aptidao[i]:
                continue
            parents_list.append(elite[i])
            if len(parents_list) == 2:
                break_flag = True
                break
        if break_flag:
            break
    return parents_list


def crossover(graph: nx.Graph, elite: list[list[int]]) -> list[int]:
    parents_list = select_parents(graph, elite)
    
    while True:
        indexMaior = random.randint(0, len(elite[0])-1)
        indexMenor = random.randint(0, len(elite[0])-1)
        if indexMenor > indexMaior:
            indexMenor, indexMaior = indexMaior, indexMenor
        
        continue_flag = False
        new_individual = [0 for _ in elite[0]]
        for i in range(0, indexMenor):
            new_individual[i] = parents_list[0][i]
        for j in range(indexMaior+1, len(elite[0])):
            new_individual[j] = parents_list[0][j]
        for k in range(indexMenor, indexMaior+1):
            if(parents_list[1][k] in new_individual):
                continue_flag = True
                break
            new_individual[k] = parents_list[1][k]
        # print(new_individual)
        if continue_flag:
            continue
        break
    
    new_individual[-1] = new_individual[0]
    return new_individual
    
def elitismo(graph: nx.Graph, population: list[list[int]]) -> list[list[int]]:
    numSelecionados = int(POPULATION_SIZE * ELITE_PERCENTAGE)
    elite = []
    population_copy = population.copy()
    while(len(elite) < numSelecionados):
        index = 0
        minimo = fitnessFuction(graph, population_copy[0])
        for i in range(len(population_copy)):
            if minimo > fitnessFuction(graph, population_copy[i]):
                minimo = fitnessFuction(graph, population_copy[i])
                index = i
        elite.append(population_copy[index])
        del population_copy[index]
    return elite
            

def main():   
    grafo: nx.Graph = nx.read_gml('PCV.gml')
    populacao = generate_population(grafo, POPULATION_SIZE)
    for i in range(50):
        elite = elitismo(grafo, populacao)
        fitness_elite = [fitnessFuction(grafo, individuo) for individuo in elite]
        lenght_elite = len(elite)
        new_population = [] + elite
        print(f"elite: {elite}")
        # print(fitness_elite)
        print("teste")
        while lenght_elite < POPULATION_SIZE:
            new_individual = mutate(grafo, crossover(grafo, elite))
            new_population.append(new_individual)
            lenght_elite += 1
        populacao = new_population
        print(f"Iteração {i}:")
        print(populacao)
        lista_fitness = [fitnessFuction(grafo, individuo) for individuo in populacao]
        print(lista_fitness)

        
    # populacao_mutada = [mutate(grafo, individuo) for individuo in populacao]
    # fitness_mutada = [fitnessFuction(grafo, individuo) for individuo in populacao_mutada]
    # print("POS MUTACAO:")
    # print(populacao_mutada)
    # print(fitness_mutada)

    pos = nx.spring_layout(grafo)
    labels = nx.get_edge_attributes(grafo, 'peso')
    nx.draw(grafo, pos, with_labels=True, node_size=700, node_color='skyblue', font_weight='bold')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
    plt.show()

main()