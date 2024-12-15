import math
import random
import numpy as np
from copy import deepcopy
from validator import *
from genetic_to_package import *

class EMS:
    """
    EMS (Empty Space) represents a vacant volume in a container where a box can potentially be placed.
    
    Attributes:
        origin (np.array): The origin point of the EMS.
        length (int): The length of the EMS.
        height (int): The height of the EMS.
        width (int): The width of the EMS.
    """
    def __init__(self, origin, length, height, width):
        """
        Initializes an EMS object.
        
        Args:
            origin (list): The origin coordinates of the EMS.
            length (int): The length of the EMS.
            height (int): The height of the EMS.
            width (int): The width of the EMS.
        """
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)

    def is_valid(self):
        """
        Checks if the EMS has valid dimensions (i.e., all dimensions must be greater than zero).
        
        Returns:
            bool: True if EMS is valid, False otherwise.
        """
        return self.length > 0 and self.height > 0 and self.width > 0
    
    def is_inside(self, other):
        """
        Checks if the current EMS is completely inside another EMS.
        
        Args:
            other (EMS): The other EMS object to compare against.
        
        Returns:
            bool: True if the current EMS is inside the other EMS, False otherwise.
        """
        return np.all(self.origin >= other.origin) and np.all(self.origin + np.array([self.length, self.height, self.width]) <= other.origin + np.array([other.length, other.height, other.width]))
    
    def if_box_fits(self, box):
        """
        Checks if a given box can fit in the EMS.
        
        Args:
            box (Box): The box to check for fitting.
        
        Returns:
            bool: True if the box can fit in the EMS, False otherwise.
        """
        fit_original = (box.length <= self.length and box.height <= self.height and box.width <= self.width)
        fit_rotated1 = (box.height <= self.length and box.length <= self.height and box.width <= self.width)
        fit_rotated2 = (box.width <= self.length and box.height <= self.height and box.length <= self.width)
        return (fit_original or fit_rotated1 or fit_rotated2)
    
    def distance_to_origin(self):
        """
        Calculates the Euclidean distance of the EMS origin from the origin (0,0,0).
        
        Returns:
            float: The Euclidean distance to the origin.
        """
        return math.sqrt(np.sum(self.origin**2))
    
    def __repr__(self):
        """
        String representation of the EMS object.
        
        Returns:
            str: The string representation of the EMS.
        """
        return f"EMS(origin={self.origin}, length={self.length}, height={self.height}, width={self.width})"
    
    def if_box_outside(self, box):
        """
        Checks if a given box is outside the EMS.
        
        Args:
            box (Box): The box to check for being outside the EMS.
        
        Returns:
            bool: True if the box is outside the EMS, False otherwise.
        """
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
    """
    Sorts a list of EMS objects based on their distance to the origin.
    
    Args:
        ems_list (list): A list of EMS objects.
        
    Returns:
        list: The sorted list of EMS objects based on their distance to the origin.
    """
    distances = [ems.distance_to_origin() for ems in ems_list]
    ems_order = np.argsort(distances)
    new_ems_list = [ems_list[i] for i in ems_order]
    return new_ems_list

class Box:
    """
    Box represents a physical box with dimensions and an optional weight.
    
    Attributes:
        origin (np.array): The origin point of the box.
        length (int): The length of the box.
        height (int): The height of the box.
        width (int): The width of the box.
        weight (int): The weight of the box.
    """
    def __init__(self, length, height, width, origin=None, weight=0):
        """
        Initializes a Box object.
        
        Args:
            length (int): The length of the box.
            height (int): The height of the box.
            width (int): The width of the box.
            origin (list, optional): The origin coordinates of the box. Defaults to [0, 0, 0].
            weight (int, optional): The weight of the box. Defaults to 0.
        """
        if origin is None:
            origin = [0, 0, 0]
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)
        self.weight = int(weight)

    def __repr__(self):
        """
        String representation of the Box object.
        
        Returns:
            str: The string representation of the Box.
        """
        return f"Box(length={self.length}, height={self.height}, width={self.width}, origin={self.origin}, weight={self.weight})"
    
    def is_equal_to_ems(self, ems):
        """
        Checks if the box is identical to a given EMS (in terms of dimensions and origin).
        
        Args:
            ems (EMS): The EMS object to compare against.
        
        Returns:
            bool: True if the box is equal to the EMS, False otherwise.
        """
        box_equals_ems = (np.all(self.origin == ems.origin) and
                          self.length == ems.length and
                          self.height == ems.height and
                          self.width == ems.width)
        return box_equals_ems


class Container:
    """
    Container represents a storage unit with multiple EMS (empty spaces) where boxes can be packed.
    
    Attributes:
        origin (np.array): The origin point of the container.
        length (int): The length of the container.
        height (int): The height of the container.
        width (int): The width of the container.
        ems (list): A list of EMS objects within the container.
    """
    def __init__(self, length, height, width, origin=None):
        """
        Initializes a Container object.
        
        Args:
            length (int): The length of the container.
            height (int): The height of the container.
            width (int): The width of the container.
            origin (list, optional): The origin coordinates of the container. Defaults to [0, 0, 0].
        """
        if origin is None:
            origin = [0, 0, 0]
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)
        self.ems = [EMS(self.origin, self.length, self.height, self.width)]

    def __repr__(self):
        """
        String representation of the Container object.
        
        Returns:
            str: The string representation of the Container.
        """
        return f"Container(length={self.length}, height={self.height}, width={self.width}, origin={self.origin})"
    
    def if_box_outside(self, box):
        """
        Checks if a given box is outside the container.
        
        Args:
            box (Box): The box to check for being outside the container.
        
        Returns:
            bool: True if the box is outside the container, False otherwise.
        """
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
    """
    Returns the volume of an object (box or container).
    
    Args:
        obj (Box or Container): The object for which volume needs to be calculated.
        
    Returns:
        int: The volume of the object.
    """
    return obj.length * obj.height * obj.width



class Chromosome:   
    def __init__(self, bps, cls):
        """
        Initialize a Chromosome object with a box packing sequence and a container loading sequence.

        Parameters:
        bps (list): The box packing sequence.
        cls (list): The container loading sequence.
        """
        self.box_packing_sequence = bps
        self.container_loading_sequence = cls

    def __repr__(self):
        """
        Return a string representation of the Chromosome object.
        """
        return f"Chromosome(Box Packing Sequence={self.box_packing_sequence}, Container Loading Sequence={self.container_loading_sequence})"

    def bps(self):
        """
        Return the box packing sequence of the Chromosome.

        Returns:
        list: The box packing sequence.
        """
        return self.box_packing_sequence

    def cls(self):
        """
        Return the container loading sequence of the Chromosome.

        Returns:
        list: The container loading sequence.
        """
        return self.container_loading_sequence


class GeneticAlgorithm(object):
    def __init__(self, uld_dimensions, package_dimensions, verbose=False):
        """
        Initialize the GeneticAlgorithm object.

        Parameters:
        uld_dimensions (list): List of ULD dimensions (length, width, height).
        package_dimensions (list): List of package dimensions (length, width, height).
        verbose (bool): Whether to print detailed logs.
        """
        self.verbose = verbose
        self.uld_dimensions = [Container(length=c[0], width=c[1], height=c[2]) for c in uld_dimensions]
        self.package_dimensions = [Box(length=b[0], width=b[1], height=b[2]) for b in package_dimensions]
        self.uld_dimensions_dict = {uld[3]: (uld[0], uld[1], uld[2]) for uld in uld_dimensions}
        self.package_dimensions_dict = {package[3]: (package[0], package[1], package[2]) for package in package_dimensions}

    def log(self, message):
        """
        Print a log message if verbose mode is enabled.

        Parameters:
        message (str): The message to log.
        """
        if self.verbose:
            print(message)

    def fitness_score(self, packing_solution):
        """
        Calculate the fitness score of a packing solution. The fitness score is based on the ratio of used container volume 
        to total container volume.

        Parameters:
        packing_solution (list): The packing solution (list of containers and boxes).

        Returns:
        float: The fitness score of the packing solution.
        """
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
        """
        Generate a list of possible empty spaces (EMS) where a box can be placed inside a container.

        Parameters:
        container (Container): The container object.
        box (Box): The box object.

        Returns:
        list: A list of valid EMS objects.
        """
        if container.if_box_outside(box):
            return []

        ems_list = []
        container_end = np.array([container.origin[0] + container.length, 
                                  container.origin[1] + container.height, 
                                  container.origin[2] + container.width])

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
    
    def update_ems(self, ems_list, box):
        """
        Update the list of empty spaces (EMS) after placing a box in the container.

        Parameters:
        ems_list (list): The current list of EMS objects.
        box (Box): The box that has been placed.

        Returns:
        list: The updated list of EMS objects.
        """
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
        """
        Filter the list of EMS objects to remove redundant spaces.

        Parameters:
        ems_list (list): The list of EMS objects.

        Returns:
        list: The filtered list of EMS objects.
        """
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
        """
        Select the best placement for a box within an EMS by considering different rotations.

        Parameters:
        box (Box): The box to be placed.
        ems (EMS): The EMS where the box is to be placed.

        Returns:
        Box: The rotated box with the best fit within the EMS.
        """
        rotations = [
            (box.length, box.height, box.width),
            (box.height, box.length, box.width),         
            (box.width, box.height, box.length)        
        ]

        possible_rotations, possible_margins = [], []

        for l, h, w in rotations:
            if l <= ems.length and h <= ems.height and w <= ems.width:
                margins = [ems.length - l, ems.height - h, ems.width - w]
                possible_rotations.append(Box(l, h, w, origin=box.origin, weight=box.weight))
                possible_margins.append(margins)

        best_ind = np.argmin([min(m) for m in possible_margins])
        return possible_rotations[best_ind]
    
    def pack_boxes(self, boxes, containers, box_packing_sequence, container_loading_sequence):
        """
        Perform the box packing process by placing boxes into containers according to the given sequences.

        Parameters:
        boxes (list): The list of box objects.
        containers (list): The list of container objects.
        box_packing_sequence (list): The sequence of boxes to be packed.
        container_loading_sequence (list): The sequence of containers to be loaded.

        Returns:
        list: The packing solution (list of containers with packed boxes).
        """
        n_containers, n_boxes = len(containers), len(boxes)

        packing_solution = []
        for c in containers:
            packing_solution.append([deepcopy(c)])

        placed_boxes = [False]*n_boxes

        for con_i in range(n_containers):
            container_ind = container_loading_sequence[con_i] -1 
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
        """
        Creates a new chromosome for the genetic algorithm.
        
        Args:
            n_boxes (int): Number of boxes.
            n_containers (int): Number of containers.

        Returns:
            Chromosome: A new chromosome with random box packing and container loading sequences.
        """
        random_box_packing_sequence = random.sample(range(1, n_boxes + 1), n_boxes)
        random_container_loading_sequence = random.sample(range(1, n_containers + 1), n_containers)
        return Chromosome(random_box_packing_sequence, random_container_loading_sequence)

    def chromosome_initialization_by_order(self, boxes, n_containers):
        """
        Initializes chromosomes based on sorting boxes by different criteria.

        Args:
            boxes (list): List of box dimensions.
            n_containers (int): Number of containers.

        Returns:
            list: A list of chromosomes sorted by box dimensions or volume.
        """
        boxes_length = [b.length for b in boxes]
        boxes_width = [b.width for b in boxes]
        boxes_height = [b.height for b in boxes]
        boxes_volume = [b.length * b.height * b.width for b in boxes]

        chromosomes = []
        for criteria in [boxes_width, boxes_height, boxes_length, boxes_volume]:
            ind = sorted(range(len(boxes)), key=lambda i: criteria[i], reverse=True)
            box_packing_sequence = [i + 1 for i in ind]
            container_loading_sequence = random.sample(range(1, n_containers + 1), n_containers)
            chromosomes.append(Chromosome(box_packing_sequence, container_loading_sequence))

        return chromosomes

    def initialize_population(self, population_size, n_containers, boxes):
        """
        Initializes the population of chromosomes for the genetic algorithm.

        Args:
            population_size (int): Desired population size.
            n_containers (int): Number of containers.
            boxes (list): List of box dimensions.

        Returns:
            list: The initialized population of chromosomes.
        """
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
        """
        Selects the top-performing chromosomes based on fitness scores.

        Args:
            fitness (list): List of fitness scores.
            elitism_size (int): Number of top chromosomes to select.

        Returns:
            list: Indices of the top-performing chromosomes.
        """
        sorted_ind = np.argsort(fitness)  # ascending
        return sorted_ind[:elitism_size]

    def selection(self, population, fitness):
        """
        Performs tournament selection to choose chromosomes for the next generation.

        Args:
            population (list): List of chromosomes.
            fitness (list): Corresponding fitness scores.

        Returns:
            list: The selected population for the next generation.
        """
        assert len(population) == len(fitness)

        population_size = len(population)
        new_population = []

        for _ in range(population_size):
            cind = random.sample(range(population_size), 2)
            better = cind[0] if fitness[cind[0]] < fitness[cind[1]] else cind[1]
            new_population.append(population[better])

        return new_population

    def mutate(self, chromosome):
        """
        Applies mutation to a chromosome by swapping elements in box packing and container loading sequences.

        Args:
            chromosome (Chromosome): The chromosome to mutate.

        Returns:
            Chromosome: A mutated chromosome.
        """
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
        """
        Performs mutation on the population based on a mutation probability.

        Args:
            population (list): The population of chromosomes.
            mutation_prob (float): Probability of mutation.

        Returns:
            list: The new population after applying mutation.
        """
        new_population = []
        for chromosome in population:
            if random.random() < mutation_prob:
                new_population.append(self.mutate(chromosome))
            else:
                new_population.append(chromosome)
        return new_population

    def crossover(self, parent1, parent2):
        """
        Performs crossover between two parent chromosomes to produce offspring.

        Args:
            parent1 (Chromosome): The first parent.
            parent2 (Chromosome): The second parent.

        Returns:
            Chromosome: The offspring produced by crossover.
        """
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
        """
        Performs crossover on a mating pool of chromosomes to generate a new population.

        Args:
            mating_pool (list): List of Chromosome objects selected for crossover.
            probability (float): The probability of performing crossover between two chromosomes.

        Returns:
            list: New population of Chromosome objects after crossover.
        """
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
        """
        Executes the genetic algorithm for optimizing box packing into containers.

        Args:
            n_iter (int): Number of iterations to run the genetic algorithm.
            population_size (int): Size of the population to maintain in each generation.
            elitism_size (int): Number of top-performing chromosomes to retain for elitism.
            crossover_prob (float): Probability of performing crossover during reproduction.
            mutation_prob (float): Probability of mutating a chromosome.

        Returns:
            list: A representation of the best solution for packing boxes into containers.
        """
        containers = self.uld_dimensions
        boxes = self.package_dimensions

        # Initialize the population
        population = self.initialize_population(population_size, len(containers), boxes)
        elitism_chromosomes, elitism_fitness = [], []

        for _ in range(n_iter):
            self.log(f"Iteration {_} of {n_iter} in Genetic Algorithm")
            
            # Evaluate fitness of each chromosome
            box_packings = [self.pack_boxes(boxes, containers, chrom.bps(), chrom.cls()) for chrom in population]
            fitness_scores = [self.fitness_score(box_packing) for box_packing in box_packings]

            # Include previous elitism chromosomes
            population += elitism_chromosomes
            fitness_scores += elitism_fitness

            # Select elitism chromosomes
            top_indices = self.elitism(fitness_scores, elitism_size)
            elitism_chromosomes = [population[i] for i in top_indices]
            elitism_fitness = [fitness_scores[i] for i in top_indices]

            if _ < n_iter - 1:
                # Remove elitism chromosomes for next generation
                remaining_indices = [i for i in range(len(population)) if i not in top_indices]
                population = [population[i] for i in remaining_indices]
                fitness_scores = [fitness_scores[i] for i in remaining_indices]

                # Generate new population through selection, crossover, and mutation
                mating_pool = self.selection(population, fitness_scores)
                crossovered_chromosomes = self.perform_crossover(mating_pool, crossover_prob)
                population = self.perform_mutation(crossovered_chromosomes, mutation_prob)

        # Identify and return the best solution
        best_index = np.argmin(fitness_scores)
        best_solution = self.pack_boxes(boxes, containers, population[best_index].bps(), population[best_index].cls())
        return best_solution

    def run_genetic_algorithm(self, n_iter=1, population_size=2, elitism_size=5, crossover_prob=0.5, mutation_prob=0.5):
        """
        Runs the complete genetic algorithm for box packing optimization.

        Args:
            n_iter (int): Number of iterations for the genetic algorithm.
            population_size (int): Number of chromosomes in the population.
            elitism_size (int): Number of top chromosomes to retain for elitism.
            crossover_prob (float): Probability of crossover in the mating pool.
            mutation_prob (float): Probability of mutation for each chromosome.

        Returns:
            PackageMatcher: An object that matches packages to containers based on the optimal packing solution.
        """
        packing_solution = self.perform_box_packing(n_iter, population_size, elitism_size, crossover_prob, mutation_prob)
        self.log("Genetic Algorithm completed")
        self.log("Processing Best Found Solution into a ULD-Package Matching")

        # Generate a package-to-container matching solution
        package_matcher = PackageMatcher(
            packing_solution=packing_solution,
            uld_ids=self.uld_dimensions_dict,
            package_ids=self.package_dimensions_dict
        )

        return package_matcher

