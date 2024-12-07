import math
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from copy import deepcopy
from uld import ULD
from cuboid import Cuboid
from package import Package
from validator import *
import itertools
from genetic_to_package import *

class EMS:
    def __init__(self, origin, length, height, width):
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)
        
    def is_valid(self):
        return self.length > 0 and self.height > 0 and self.width > 0
    
    def is_inside(self, other):
        return np.all(self.origin >= other.origin) and np.all(self.origin + np.array([self.length, self.height, self.width]) <= other.origin + np.array([other.length, other.height, other.width]))
    
    def if_box_fits(self, box):
        fit_original = (box.length <= self.length and box.height <= self.height and box.width <= self.width)
        fit_rotated1 = (box.height <= self.length and box.length <= self.height and box.width <= self.width)
        fit_rotated2 = (box.width <= self.length and box.height <= self.height and box.length <= self.width)
        return (fit_original or fit_rotated1 or fit_rotated2)
    
    
    def distance_to_origin(self):
        return math.sqrt(np.sum(self.origin**2))
    
    
    def __repr__(self):
        return f"EMS(origin={self.origin}, length={self.length}, height={self.height}, width={self.width})"
    
    def if_box_outside(self, box):
        container_vertex1 = self.origin
        container_vertex2 = self.origin + np.array([self.length, self.height, self.width])

        box_vertex1 = box.origin
        box_vertex2 = box.origin + np.array([0, box.height, 0])
        box_vertex3 = box.origin + np.array([0, 0, box.width])
        box_vertex4 = box.origin + np.array([box.length, 0, 0])
        
        is_outside = ((container_vertex1[1] >= box_vertex2[1]) or
                    (container_vertex2[1] <= box_vertex1[1]) or
                    (container_vertex2[0] <= box_vertex1[0]) or
                    (container_vertex1[0] >= box_vertex4[0]) or
                    (container_vertex1[2] >= box_vertex3[2]) or
                    (container_vertex2[2] <= box_vertex1[2]))

        return is_outside
    
def prioritize_ems(ems_list):
    distances = [ems.distance_to_origin() for ems in ems_list]
    ems_order = np.argsort(distances)
    new_ems_list = [ems_list[i] for i in ems_order]
    return new_ems_list

class Box:
    def __init__(self, length, height, width, origin=None, weight=0):
        if origin is None:
            origin = [0, 0, 0]
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)
        self.weight = int(weight)
        if self.length <= 0 or self.height <= 0 or self.width <= 0:
            raise Exception("A number <= 0 for one of the parameters was given for Box.")
    
    def __repr__(self):
        return f"Box(length={self.length}, height={self.height}, width={self.width}, origin={self.origin}, weight={self.weight})"
    
    def is_equal_to_ems(self, ems):
        box_equals_ems = (np.all(self.origin == ems.origin) and
                          self.length == ems.length and
                          self.height == ems.height and
                          self.width == ems.width)
        return box_equals_ems
    

    
    
class Container:
    def __init__(self, length, height, width, origin=None):
        if origin is None:
            origin = [0,0,0]
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)
        if self.length <= 0 or self.height <= 0 or self.width <= 0:
            raise Exception("A number <= 0 for one of the parameters was given for Container.")
        # initial EMS is the whole container
        self.ems = [EMS(self.origin, self.length, self.height, self.width)]
    def __repr__(self):
        return f"Container(length={self.length}, height={self.height}, width={self.width}, origin={self.origin})"

    def if_box_outside(self, box):
        container_vertex1 = self.origin
        container_vertex2 = self.origin + np.array([self.length, self.height, self.width])

        box_vertex1 = box.origin
        box_vertex2 = box.origin + np.array([0, box.height, 0])
        box_vertex3 = box.origin + np.array([0, 0, box.width])
        box_vertex4 = box.origin + np.array([box.length, 0, 0])
        
        is_outside = ((container_vertex1[1] >= box_vertex2[1]) or
                    (container_vertex2[1] <= box_vertex1[1]) or
                    (container_vertex2[0] <= box_vertex1[0]) or
                    (container_vertex1[0] >= box_vertex4[0]) or
                    (container_vertex1[2] >= box_vertex3[2]) or
                    (container_vertex2[2] <= box_vertex1[2]))

        return is_outside
    
def volume(obj):
    return obj.length * obj.height * obj.width


class Chromosome:   
    def __init__(self, bps, cls):
        self.box_packing_sequence = bps
        self.container_loading_sequence = cls

    def __repr__(self):
        return f"Chromosome(Box Packing Sequence={self.box_packing_sequence}, Container Loading Sequence={self.container_loading_sequence})"

    def bps(self):
        return self.box_packing_sequence

    def cls(self):
        return self.container_loading_sequence

class GeneticAlgorithm(object):
    def __init__(self, uld_dimensions, package_dimensions):
        self.uld_dimensions = [Container(length=c[0], width=c[1], height=c[2]) for c in uld_dimensions]
        self.package_dimensions = [Box(length=b[0], width=b[1], height=b[2]) for b in package_dimensions]
        
        self.uld_dimensions_dict = {uld[3]: (uld[0], uld[1], uld[2]) for uld in uld_dimensions}
        self.package_dimensions_dict = {package[3]: (package[0], package[1], package[2]) for package in package_dimensions}
        
    def fitness_score(self, packing_solution):
        container_volume = 0
        boxes_volume = 0

        for ps in packing_solution:
            if len(ps) == 1:
                continue
            else:
                container_volume += volume(ps[0])
                for b in ps[1:]:
                    boxes_volume += volume(b)


        fitness = 1 - (boxes_volume / container_volume)
        return fitness
    
    def EMS_list(self, container, box):
        if container.if_box_outside(box):
            return []

        ems_list = []
        container_end = np.array([container.origin[0] + container.length, 
                                container.origin[1] + container.height, 
                                container.origin[2] + container.width])

        # Define EMS regions
        ems_candidates = [
            EMS(origin=container.origin, 
                length=box.origin[0] - container.origin[0], 
                height=container.height, 
                width=container.width),
            EMS(origin=container.origin, 
                length=container.length, 
                height=container.height, 
                width=box.origin[2] - container.origin[2]),
            EMS(origin=np.array([box.origin[0]+box.length, container.origin[1], container.origin[2]]),
                length=container.origin[0] + container.length - (box.origin[0] + box.length), 
                height=container.height, 
                width=container.width),
            EMS(origin=np.array([container.origin[0], container.origin[1], box.origin[2]+box.width]),
                length=container.length, 
                height=container.height, 
                width=container_end[2] - (box.origin[2] + box.width)),
            EMS(origin=np.array([container.origin[0], box.origin[1]+box.height, container.origin[2]]),
                length=container.length, 
                height=container_end[1] - (box.origin[1] + box.height), 
                width=container.width),
            EMS(origin=container.origin, 
                length=container.length, 
                height=box.origin[1] - container.origin[1], 
                width=container.width)
        ]

        ems_list = [ems for ems in ems_candidates if (ems).is_valid()]
        return ems_list
    
    def update_ems(self, ems_list,box):
        new_ems_list = ems_list[:]
        ind_to_remove = []

        for i in range(len(ems_list)):
            ems = ems_list[i]
            new_ems = self.EMS_list(ems, box)
            
            if len(new_ems) != 0 or box.is_equal_to_ems(ems):
                ind_to_remove.append(i)
                for ne in new_ems:
                    new_ems_list.append(ne)

        if len(ind_to_remove) != 0:
            new_ems_list = [new_ems_list[k] for k in range(len(new_ems_list)) if k not in ind_to_remove]

        filtered_ems_list = self.filter_ems_list(new_ems_list)

        return filtered_ems_list
    
    def filter_ems_list(self, ems_list):
        sequence = list(range(len(ems_list)))
        ind_remove = []

        for i in sequence:
            ems_i = ems_list[i]
            for j in sequence:
                if i == j:
                    continue
                if ems_i.is_inside(ems_list[j]):
                    ind_remove.append(i)
                    break

        if len(ind_remove) != 0:
            ems_list = [ems_list[k] for k in range(len(ems_list)) if k not in ind_remove]

        return ems_list
    


    def placement_selection(self, box, ems):
        rotations = [
            (box.length, box.height, box.width),          # Original orientation
            (box.height, box.length, box.width),         # Rotation 1: Swap length & height
            (box.width, box.height, box.length)          # Rotation 2: Swap length & width
        ]

        possible_rotations, possible_margins = [], []

        for l, h, w in rotations:
            if l <= ems.length and h <= ems.height and w <= ems.width:
                margins = [ems.length - l, ems.height - h, ems.width - w]
                possible_rotations.append(Box(l, h, w, origin=box.origin, weight=box.weight))
                possible_margins.append(margins)

        if not possible_rotations:
            raise Exception('The box does not fit into the EMS')

        best_ind = np.argmin([min(m) for m in possible_margins])
        return possible_rotations[best_ind]
    
    
    def pack_boxes(self, boxes, containers, box_packing_sequence, container_loading_sequence):
        n_containers, n_boxes = len(containers), len(boxes)
        
        if n_containers == 0 or n_boxes == 0:
            raise Exception('Specify at least one container and one box')

        packing_solution = []
        for c in containers:
            packing_solution.append([deepcopy(c)])

        placed_boxes = [False]*n_boxes

        for con_i in range(n_containers):
            container_ind = container_loading_sequence[con_i] -1  # -1 for 0-based index
            for box_i in range(n_boxes):
                box_ind = box_packing_sequence[box_i] -1
                if placed_boxes[box_ind]:
                    continue
                else:
                    box = boxes[box_ind]
                    con_EMS = packing_solution[container_ind][0].ems
                    new_con_EMS = prioritize_ems(con_EMS)
                    for ems in new_con_EMS:
                        if ems.if_box_fits(box):
                            new_box_with_placement = self.placement_selection(box, ems)
                            new_box_with_placement.origin = ems.origin.copy()
                            if packing_solution[container_ind][0].if_box_outside(new_box_with_placement):
                                continue

                            packing_solution[container_ind].append(new_box_with_placement)

                            packing_solution[container_ind][0].ems = self.update_ems(packing_solution[container_ind][0].ems, new_box_with_placement)
                            placed_boxes[box_ind] = True
                            break
        return packing_solution
    



    def create_chromosome(self, n_boxes, n_containers):
        random_box_packing_sequence = random.sample(range(1, n_boxes+1), n_boxes)
        random_container_loading_sequence = random.sample(range(1, n_containers+1), n_containers)
        return Chromosome(random_box_packing_sequence, random_container_loading_sequence)

    def chromosome_initialization_by_order(self, boxes, n_containers):
        boxes_length = [b.length for b in boxes]
        boxes_width = [b.width for b in boxes]
        boxes_height = [b.height for b in boxes]
        boxes_volume = [b.length*b.height*b.width for b in boxes]
        
        chromosomes = []
        
        for criteria in [boxes_width, boxes_height, boxes_length, boxes_volume]:
            ind = sorted(range(len(boxes)), key=lambda i: criteria[i], reverse=True)
            box_packing_sequence = [i+1 for i in ind]
            container_loading_sequence = random.sample(range(1, n_containers+1), n_containers)
            chromosomes.append(Chromosome(box_packing_sequence, container_loading_sequence))        

        return chromosomes

    def initialize_population(self, population_size, n_containers, boxes):
        population = self.chromosome_initialization_by_order(boxes, n_containers)
        if population_size <= 4:
            population = population[:population_size]
        else:
            to_create = population_size - 4
            for _ in range(to_create):
                new_chromosome = self.create_chromosome(len(boxes), n_containers)
                population.append(new_chromosome)
        return population

    def elitism(self, fitness, elitism_size):
        sorted_ind = np.argsort(fitness)  # ascending
        return sorted_ind[:elitism_size]

    def selection(self, population, fitness):
        assert len(population) == len(fitness)
        
        population_size = len(population)
        new_population = []
        
        for _ in range(population_size):
            cind = random.sample(range(population_size), 2)
            better = cind[0] if fitness[cind[0]] < fitness[cind[1]] else cind[1]
            new_population.append(population[better])
            
        return new_population

    def mutate(self, chromosome):
        bps = chromosome.bps()
        cls = chromosome.cls()
        
        num_boxes, num_containers = len(bps), len(cls)

        if num_boxes <= 2:
            bps.reverse()
        else:
            idx1, idx2 = random.sample(range(num_boxes), 2)
            bps[idx1], bps[idx2] = bps[idx2], bps[idx1]

        if num_containers <= 2:
            cls.reverse()
        else:
            idx1, idx2 = random.sample(range(num_containers), 2)
            cls[idx1], cls[idx2] = cls[idx2], cls[idx1]

        return Chromosome(bps, cls)

    def perform_mutation(self, population, mutation_prob):
        new_population = []
        for chromosome in population:
            if random.random() < mutation_prob:
                new_population.append(self.mutate(chromosome))
            else:
                new_population.append(chromosome)
        return new_population

    def crossover(self, parent1, parent2):
        bps1, cls1 = parent1.bps(), parent1.cls()
        bps2, cls2 = parent2.bps(), parent2.cls()
        
        assert len(bps1) == len(bps2) and len(cls1) == len(cls2)
        
        n_boxes, n_containers = len(bps1), len(cls1)

        cut_box_i, cut_box_j = sorted(random.sample(range(n_boxes), 2))
        cut_con_i, cut_con_j = sorted(random.sample(range(n_containers), 2))

        child_BPS = [bps1[x] if cut_box_i < x <= cut_box_j else 0 for x in range(n_boxes)]
        child_CLS = [cls1[x] if cut_con_i < x <= cut_con_j else 0 for x in range(n_containers)]

        def fill_missing(child, parent2, cut_i, cut_j, n):
            missing = [g for g in parent2 if g not in set(child) - {0}]
            fill_positions = list(range(cut_j + 1, n)) + list(range(cut_i + 1))
            for pos in fill_positions:
                if child[pos] == 0:
                    child[pos] = missing.pop(0)

        fill_missing(child_BPS, bps2, cut_box_i, cut_box_j, n_boxes)
        fill_missing(child_CLS, cls2, cut_con_i, cut_con_j, n_containers)

        return Chromosome(child_BPS, child_CLS)


    def perform_crossover(self, mating_pool, probability):
        new_population = []

        while len(mating_pool) > 1:
            parent1, parent2 = random.sample(mating_pool, 2)
            mating_pool.remove(parent1)
            mating_pool.remove(parent2)

            if random.random() < probability:
                new_population.extend([self.crossover(parent1, parent2), self.crossover(parent2, parent1)])
            else:
                new_population.extend([parent1, parent2])

        if mating_pool:
            new_population.append(mating_pool.pop())

        return new_population


    def perform_box_packing(self, n_iter, population_size, elitism_size, crossover_prob, mutation_prob):
        if elitism_size < 0 or n_iter <= 0 or population_size <= 0:
            raise ValueError("Invalid parameters: Ensure non-negative elitism_size and positive iterations/population size.")
        if not 0 <= crossover_prob <= 1 or not 0 <= mutation_prob <= 1:
            raise ValueError("Probabilities must be in the range [0, 1].")
        
        containers = self.uld_dimensions
        boxes = self.package_dimensions
        
        if not containers or not boxes:
            raise ValueError("Specify at least one container and one box.")

        population = self.initialize_population(population_size, len(containers), boxes)
        elitism_chromosomes, elitism_fitness = [], []

        for _ in range(n_iter):
            box_packings = [self.pack_boxes(boxes, containers, chrom.bps(), chrom.cls()) for chrom in population]
            fitness_scores = [self.fitness_score(box_packing) for box_packing in box_packings]
            population += elitism_chromosomes
            fitness_scores += elitism_fitness
            top_indices = self.elitism(fitness_scores, elitism_size)
            
            elitism_chromosomes = [population[i] for i in top_indices]
            elitism_fitness = [fitness_scores[i] for i in top_indices]

            if _ < n_iter - 1:
                remaining_indices = [i for i in range(len(population)) if i not in top_indices]
                population = [population[i] for i in remaining_indices]
                fitness_scores = [fitness_scores[i] for i in remaining_indices]
            
                mating_pool = self.selection(population, fitness_scores)
                crossovered_chromosomes = self.perform_crossover(mating_pool, crossover_prob)
                population = self.perform_mutation(crossovered_chromosomes, mutation_prob)
                

        best_index = np.argmin(fitness_scores)
        best_solution = self.pack_boxes(boxes, containers, population[best_index].bps(), population[best_index].cls())
        return best_solution


    def run_genetic_algorithm(self, n_iter=1, population_size=2, elitism_size=5, crossover_prob=0.5, mutation_prob=0.5):
        packing_solution = self.perform_box_packing(n_iter, population_size, elitism_size, crossover_prob, mutation_prob)

        package_matcher = PackageMatcher(packing_solution=packing_solution, uld_ids=self.uld_dimensions_dict, package_ids=self.package_dimensions_dict)
        
        return package_matcher
        
