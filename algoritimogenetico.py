#Importações
import numpy as np
import random

from datetime import datetime

# quantidade = int(input("Digite a quantidade de cidades (mais que duase menos que 5): "))
# while quantidade < 2 or quantidade > 5:
#   print("Quantidade inválida! Deve ser maior que duas.")
#   quantidade = int(input("Digite a quantidade de cidades (mais que duas e menos que 5): "))
# tamanhoPopulacao = int(input("Digite o tamanho da população (maios que um): "))
# while tamanhoPopulacao < 1:
#   print("Quantidade inválida! Deve ser maior que um.")
#   tamanhoPopulacao = int(input("Digite o tamanho da população (maios que um): "))
# geracoes = int(input("Digite a quantidade de gerações (mais que uma): "))
# while geracoes < 1:
#   print("Quantidade inválida! Deve ser maior que um.")
#   geracoes = int(input("Digite a quantidade de gerações (mais que uma): "))

#Parâmetros
n_cities = 6 #quantidade
n_population = 20 #tamanhoPopulacao
mutation_rate = 0.3

#gerando lista de coordenadas representando cada cidade
cordinates_list = [[x,y] for x,y in zip(np.random.randint(0,100,n_cities), np.random.randint(0,100,n_cities))]
names_list = np.array(['CidadeA','CidadeB','CidadeC','CidadeD','CidadeE','CidadeF'])
cities_dict = {x:y for x,y in zip(names_list,cordinates_list)}

# Função para calcular a distância entre dois pontos
def compute_city_distance_coordinates(a,b):
  return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def compute_city_distance_names(city_a, city_b, cities_dict):
  return compute_city_distance_coordinates_fixo(cities_dict[city_a],cities_dict[city_b])

def compute_city_distance_coordinates_fixo(a,b):
  for i in range(len(names_list)):
    if a == names_list[i] and b == names_list[i]:
      return 0
    if i < 5:
      if a == names_list[i] and b == names_list[i+1] or a == names_list[i+1] and b == names_list[i]:
        return 1
      if i < 4:
        if a == names_list[i] and b == names_list[i+2] or a == names_list[i+2] and b == names_list[i]:
          return 2
        if i < 3:
          if a == names_list[i] and b == names_list[i+3] or a == names_list[i+3] and b == names_list[i]:
            return 3
          if i < 2:
            if a == names_list[i] and b == names_list[i+4] or a == names_list[i+4] and b == names_list[i]:
              return 1
            if i < 1:
              if a == names_list[i] and b == names_list[i+5] or a == names_list[i+5] and b == names_list[i]:
                return 2

def compute_city_distance_names_fixo(city_a, city_b, cities_dict):
  return compute_city_distance_coordinates_fixo(city_a, city_b)

cities_dict

#criar a primeira população
def genesis(city_list, n_population):
  population_set = []
  for i in range(n_population):
    sol_i = city_list[np.random.choice(list(range(n_cities)), n_cities, replace=False)]
    population_set.append(sol_i)
  return np.array(population_set)  
population_set = genesis(names_list, n_population)
population_set

def fitnes_eval(city_list, cities_dict):
  total = 0
  for i in range(n_cities-1):
    a = city_list[i]
    b = city_list[i+1]
    total += compute_city_distance_names_fixo(a,b, cities_dict)
  return total

def get_all_fitnes(population_set, cities_dict):
  fitnes_list = np.zeros(n_population)

  #Loop para achar todas as soluções possíveis
  for i in range(n_population):
      fitnes_list[i] = fitnes_eval(population_set[i], cities_dict)
  return fitnes_list

fitnes_list = get_all_fitnes(population_set, cities_dict)
fitnes_list

def progenitor_selection(population_set, fitnes_list):
  #Selecionando os pais
  total_fit = fitnes_list.sum()
  prob_list = fitnes_list/total_fit

  progenitor_list_a = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list, replace=True)
  progenitor_list_b = np.random.choice(list(range(len(population_set))), len(population_set), p=prob_list, replace=True)

  progenitor_list_a = population_set[progenitor_list_a]
  progenitor_list_b = population_set[progenitor_list_b]

  return np.array([progenitor_list_a, progenitor_list_b])

progenitor_list = progenitor_selection(population_set, fitnes_list)

def mate_progenitors(prog_a, prog_b):
  offspring = prog_a[0:5]

  for city in prog_b:
    if not city in offspring:
      offspring = np.concatenate((offspring, [city]))
  return offspring    

def mate_population(progenitor_list):
  new_population_set = []
  for i in range(progenitor_list.shape[1]):
    prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
    offspring = mate_progenitors(prog_a, prog_b)
    new_population_set.append(offspring)
  return new_population_set

new_population_set = mate_population(progenitor_list)
new_population_set[0]

def mutate_offspring(offspring):
  for q in range(int(n_cities*mutation_rate)):
    a = np.random.randint(0,n_cities)
    b = np.random.randint(0,n_cities)

    offspring[a], offspring[b] = offspring[b], offspring[a]

  return offspring

def mutate_population(new_population_set):
  mutated_pop = []
  for offspring in new_population_set:
    mutated_pop.append(mutate_offspring(offspring))
  return mutated_pop

mutated_pop = mutate_population(new_population_set)
mutated_pop[0]      

best_solution = [-1, np.inf, np.array([])]
for i in range(1000):
  if i%100 == 0: print(i, fitnes_list.min(), fitnes_list.mean(), datetime.now().strftime("%d/%m/%y %H:%M"))
  fitnes_list = get_all_fitnes(mutated_pop, cities_dict)

  if fitnes_list.min() < best_solution[1]:
    best_solution[0] = i
    best_solution[1] = fitnes_list.min()
    best_solution[2] = np.array(mutated_pop)[fitnes_list.min() == fitnes_list]

  progenitor_list = progenitor_selection(population_set, fitnes_list)
  new_population_set = mate_population(progenitor_list)

  mutated_pop = mutate_population(new_population_set)  

print(best_solution)  
