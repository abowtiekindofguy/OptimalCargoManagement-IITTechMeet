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

### Classes ###

# random.seed(123)
# np.random.seed(123)

class EMS:
    def __init__(self, origin, length, height, width):
        self.origin = np.array(origin, dtype=int)
        self.length = int(length)
        self.height = int(height)
        self.width = int(width)
    def __repr__(self):
        return f"EMS(origin={self.origin}, length={self.length}, height={self.height}, width={self.width})"

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

# class Algorithm:
def CheckIfBoxIsOutside(container, box):
    container_vertex1 = container.origin
    container_vertex2 = container.origin + np.array([container.length, container.height, container.width])

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

def CheckIfEMSvalid(EMS_object):
    if EMS_object.length <= 0 or EMS_object.height <= 0 or EMS_object.width <= 0:
        return False
    else:
        return True

def CreateEMS(container, box):
    # container = deepcopy(given_container)
    # box = deepcopy(given_box)
    if len(box.origin) == 0:
        raise Exception('Specify origin for the box')

    if CheckIfBoxIsOutside(container, box):
        return []

    ems_list = []

    # EMS 1:
    EMS1 = EMS(origin=container.origin,
            length=(box.origin[0] - container.origin[0]),
            height=container.height,
            width=container.width)
    if CheckIfEMSvalid(EMS1):
        ems_list.append(EMS1)

    # EMS 2:
    EMS2 = EMS(origin=container.origin,
            length=container.length,
            height=container.height,
            width=(box.origin[2] - container.origin[2]))
    if CheckIfEMSvalid(EMS2):
        ems_list.append(EMS2)

    # EMS 3:
    EMS3_origin = np.array([box.origin[0], container.origin[1], container.origin[2]]) + np.array([box.length, 0, 0])
    EMS3 = EMS(origin=EMS3_origin,
            length=((container.origin + np.array([container.length, 0, 0])) - EMS3_origin)[0],
            height=container.height,
            width=container.width)
    if CheckIfEMSvalid(EMS3):
        ems_list.append(EMS3)

    # EMS 4:
    EMS4_origin = np.array([container.origin[0], container.origin[1], box.origin[2]]) + np.array([0, 0, box.width])
    EMS4 = EMS(origin=EMS4_origin,
            length=container.length,
            height=container.height,
            width=((container.origin + np.array([0,0,container.width])) - EMS4_origin)[2])
    if CheckIfEMSvalid(EMS4):
        ems_list.append(EMS4)

    # EMS 5:
    EMS5_origin = np.array([container.origin[0], box.origin[1], container.origin[2]]) + np.array([0, box.height, 0])
    EMS5 = EMS(origin=EMS5_origin,
            length=container.length,
            height=((container.origin + np.array([0,container.height,0])) - EMS5_origin)[1],
            width=container.width)
    if CheckIfEMSvalid(EMS5):
        ems_list.append(EMS5)

    # EMS 6:
    EMS6 = EMS(origin=container.origin,
            length=container.length,
            height=(box.origin[1] - container.origin[1]),
            width=container.width)
    if CheckIfEMSvalid(EMS6):
        ems_list.append(EMS6)

    return ems_list

def CheckIfEMSisInsideOtherEMS(ems_to_check, ems):
    ems_to_check_vertex1 = ems_to_check.origin
    ems_to_check_vertex2 = ems_to_check.origin + np.array([ems_to_check.length, ems_to_check.height, ems_to_check.width])

    ems_vertex1 = ems.origin
    ems_vertex2 = ems.origin + np.array([ems.length, ems.height, ems.width])

    ems_is_inside = np.all(ems_to_check_vertex1 >= ems_vertex1) and np.all(ems_to_check_vertex2 <= ems_vertex2)
    return ems_is_inside

# Can Change Here #1
def EliminateEMSList(ems_list):
    # ems_list = deepcopy(given_ems_list)
    # ems_list = given_ems_list
    sequence = list(range(len(ems_list)))
    ind_remove = []

    for i in sequence:
        ems_i = ems_list[i]
        for j in sequence:
            if i == j:
                continue
            if CheckIfEMSisInsideOtherEMS(ems_i, ems_list[j]):
                ind_remove.append(i)
                break

    if len(ind_remove) != 0:
        ems_list = [ems_list[k] for k in range(len(ems_list)) if k not in ind_remove]

    return ems_list

def CheckIfBoxEqualsEMS(box, ems):
    BoxEqualsEMS = (np.all(box.origin == ems.origin) and
                    box.length == ems.length and
                    box.height == ems.height and
                    box.width == ems.width)
    return BoxEqualsEMS
#Not getting should be changed or not
def UpdateEMS(ems_list,box):
    # ems_list = deepcopy(given_ems_list)
    # box = deepcopy(given_box)

    new_ems_list = ems_list[:]
    ind_to_remove = []

    for i in range(len(ems_list)):
        # ems = deepcopy(ems_list[i])
        ems = ems_list[i]
        new_ems = CreateEMS(ems, box)
        if len(new_ems) != 0 or CheckIfBoxEqualsEMS(box, ems):
            ind_to_remove.append(i)
            for ne in new_ems:
                new_ems_list.append(ne)

    if len(ind_to_remove) != 0:
        new_ems_list = [new_ems_list[k] for k in range(len(new_ems_list)) if k not in ind_to_remove]

    new_ems_list = EliminateEMSList(new_ems_list)

    return new_ems_list

def CalculateDistanceToBoxOrigin(ems):
    return math.sqrt(np.sum(ems.origin**2))

def PrioritizeEMS(ems_list):
    # ems_list = deepcopy(given_ems_list)
    distances = [CalculateDistanceToBoxOrigin(e) for e in ems_list]
    ems_order = np.argsort(distances)
    new_ems_list = [ems_list[i] for i in ems_order]
    return new_ems_list

def CheckIfBoxFitsIntoEMS(box, ems):
    fit1 = (box.length <= ems.length and box.height <= ems.height and box.width <= ems.width)
    fit2 = (box.height <= ems.length and box.length <= ems.height and box.width <= ems.width)
    fit3 = (box.width <= ems.length and box.height <= ems.height and box.length <= ems.width)
    return (fit1 or fit2 or fit3)

def PerformPlacementSelection(box,ems):
    # box = deepcopy(given_box)
    # ems = deepcopy(given_ems)
    possible_rotations = []
    possible_margins = []

    # original fit
    if (box.length <= ems.length and box.height <= ems.height and box.width <= ems.width):
        margins_0 = [ems.length - box.length, ems.height - box.height, ems.width - box.width]
        possible_rotations.append(Box(box.length, box.height, box.width, origin=box.origin, weight=box.weight))
        possible_margins.append(margins_0)

    # rotation 1 (swap length & height)
    if (box.height <= ems.length and box.length <= ems.height and box.width <= ems.width):
        margins_1 = [ems.length - box.height, ems.height - box.length, ems.width - box.width]
        rotated_box_1 = Box(box.height, box.length, box.width, origin=box.origin, weight=box.weight)
        possible_rotations.append(rotated_box_1)
        possible_margins.append(margins_1)

    # rotation 2 (swap length & width)
    if (box.width <= ems.length and box.height <= ems.height and box.length <= ems.width):
        margins_2 = [ems.length - box.width, ems.height - box.height, ems.width - box.length]
        rotated_box_2 = Box(box.width, box.height, box.length, origin=box.origin, weight=box.weight)
        possible_rotations.append(rotated_box_2)
        possible_margins.append(margins_2)

    if len(possible_rotations) == 0:
        raise Exception('The box does not fit into the EMS')
    else:
        # select rotation with smallest min margin
        min_values = [min(m) for m in possible_margins]
        best_ind = np.argmin(min_values)
        rotated_box = possible_rotations[best_ind]

    return rotated_box

def CalculateVolume(obj):
    return obj.length * obj.height * obj.width

def PackBoxes(boxes, containers, box_packing_sequence, container_loading_sequence):
    n = len(containers)
    m = len(boxes)

    if n == 0:
        raise Exception('Specify containers')
    if m == 0:
        raise Exception('Specify boxes')

    # create empty packing solution
    packing_solution = []
    for c in containers:
        # each container solution is [container, possibly boxes...]
        packing_solution.append([deepcopy(c)])
        # packing_solution.append([c])

    placed_boxes = [False]*m

    for con_i in range(n):
        container_ind = container_loading_sequence[con_i] -1  # -1 for 0-based index
        for box_i in range(m):
            box_ind = box_packing_sequence[box_i] -1
            if placed_boxes[box_ind]:
                continue
            else:
                box = boxes[box_ind]
                con_EMS = packing_solution[container_ind][0].ems
                new_con_EMS = PrioritizeEMS(con_EMS)
                for ems in new_con_EMS:
                    if CheckIfBoxFitsIntoEMS(box, ems):
                        new_box = PerformPlacementSelection(box, ems)
                        new_box.origin = ems.origin.copy()
                        if CheckIfBoxIsOutside(packing_solution[container_ind][0], new_box):
                            continue
                        # write placement in packing solution
                        packing_solution[container_ind].append(new_box)
                        # update EMS
                        # packing_solution[container_ind][0].ems = deepcopy(UpdateEMS(packing_solution[container_ind][0].ems, new_box))
                        packing_solution[container_ind][0].ems = UpdateEMS(packing_solution[container_ind][0].ems, new_box)
                        placed_boxes[box_ind] = True
                        break
    return packing_solution

def CalculateFitness(packing_solution):
    container_volume = 0
    boxes_volume = 0

    for ps in packing_solution:
        if len(ps) == 1:
            continue
        else:
            container_volume += CalculateVolume(ps[0])
            for b in ps[1:]:
                boxes_volume += CalculateVolume(b)


    fitness = 1 - (boxes_volume / container_volume)
    return fitness


def CreateChromosome(n_boxes, n_containers):
    BPS = list(range(1,n_boxes+1))
    random.shuffle(BPS)
    CLS = list(range(1,n_containers+1))
    random.shuffle(CLS)
    return {"BPS": BPS, "CLS": CLS}

def CustomChromosomeInitialization(boxes, n_containers):
    boxes_length = [b.length for b in boxes]
    boxes_width = [b.width for b in boxes]
    boxes_height = [b.height for b in boxes]
    boxes_volume = [b.length*b.height*b.width for b in boxes]

    chromosomes = []
    # sort by length desc
    ind_by_length = sorted(range(len(boxes)), key=lambda i: boxes_length[i], reverse=True)
    chromosomes.append({"BPS":[i+1 for i in ind_by_length], "CLS":random.sample(range(1,n_containers+1), n_containers)})

    # sort by height desc
    ind_by_height = sorted(range(len(boxes)), key=lambda i: boxes_height[i], reverse=True)
    chromosomes.append({"BPS":[i+1 for i in ind_by_height], "CLS":random.sample(range(1,n_containers+1), n_containers)})
    
    # sort by width desc
    ind_by_width = sorted(range(len(boxes)), key=lambda i: boxes_width[i], reverse=True)
    chromosomes.append({"BPS":[i+1 for i in ind_by_width], "CLS":random.sample(range(1,n_containers+1), n_containers)})

    # sort by volume desc
    ind_by_volume = sorted(range(len(boxes)), key=lambda i: boxes_volume[i], reverse=True)
    chromosomes.append({"BPS":[i+1 for i in ind_by_volume], "CLS":random.sample(range(1,n_containers+1), n_containers)})

    # return deepcopy(chromosomes)
    return chromosomes

def InitializePopulation(population_size, n_containers, boxes):
    n_boxes = len(boxes)
    population = CustomChromosomeInitialization(boxes, n_containers)
    if population_size <= 4:
        population = population[:population_size]
    else:
        to_create = population_size - 4
        for _ in range(to_create):
            population.append(CreateChromosome(n_boxes, n_containers))
    return population

def PerformElitism(fitness, elitism_size):
    sorted_ind = np.argsort(fitness)  # ascending
    return sorted_ind[:elitism_size]

def PerformSelection(population, fitness):
    assert len(population) == len(fitness)
    population_size = len(population)
    new_population = []
    for _ in range(population_size):
        # population_copy = deepcopy(population)
        cind = random.sample(range(population_size), 2)
        better = cind[0] if fitness[cind[0]] < fitness[cind[1]] else cind[1]
        new_population.append(population[better])
    return new_population

def MutateChromosome(chromosome):
    # chromosome = deepcopy(given_chromosome)
    BPS = chromosome["BPS"][:]
    CLS = chromosome["CLS"][:]
    n_boxes = len(BPS)
    n_containers = len(CLS)

    if n_boxes <= 2:
        BPS.reverse()
    else:
        replace_boxes_ind = random.sample(range(n_boxes), 2)
        BPS[replace_boxes_ind[0]], BPS[replace_boxes_ind[1]] = BPS[replace_boxes_ind[1]], BPS[replace_boxes_ind[0]]

    if n_containers <= 2:
        CLS.reverse()
    else:
        replace_containers_ind = random.sample(range(n_containers), 2)
        CLS[replace_containers_ind[0]], CLS[replace_containers_ind[1]] = CLS[replace_containers_ind[1]], CLS[replace_containers_ind[0]]

    return {"BPS":BPS, "CLS":CLS}

def PerformMutation(population, mutation_prob):
    # population = deepcopy(given_population)

    population_size = len(population)
    new_population = []
    for chrom in population:
        if random.random() < mutation_prob:
            new_population.append(MutateChromosome(chrom))
        else:
            new_population.append(chrom)
    return new_population

def CrossoverChromosomes(parent1, parent2):
    # parent1 = deepcopy(gparent1)
    # parent2 = deepcopy(gparent2)
    BPS1 = parent1["BPS"]
    CLS1 = parent1["CLS"]
    BPS2 = parent2["BPS"]
    CLS2 = parent2["CLS"]
    n_boxes = len(BPS1)
    n_containers = len(CLS1)

    cutting_box_points = random.sample(range(n_boxes), 2)
    cut_box_i = min(cutting_box_points)
    cut_box_j = max(cutting_box_points)

    cutting_con_points = random.sample(range(n_containers), 2)
    cut_con_i = min(cutting_con_points)
    cut_con_j = max(cutting_con_points)

    child_BPS = [0]*n_boxes
    child_CLS = [0]*n_containers

    # copy genes between cutting points from parent1
    for x in range(cut_box_i+1, cut_box_j+1):
        child_BPS[x] = BPS1[x]
    for x in range(cut_con_i+1, cut_con_j+1):
        child_CLS[x] = CLS1[x]

    # fill missing genes in BPS
    existing = set(child_BPS) - {0}
    missing = [g for g in BPS2 if g not in existing]
    box_fill_positions = []
    if cut_box_j != n_boxes-1:
        box_fill_positions += list(range(cut_box_j+1, n_boxes))
    box_fill_positions += list(range(cut_box_i+1))
    for pos in box_fill_positions:
        if child_BPS[pos] == 0:
            child_BPS[pos] = missing.pop(0)

    # fill missing genes in CLS
    existing = set(child_CLS) - {0}
    missing = [g for g in CLS2 if g not in existing]
    con_fill_positions = []
    if cut_con_j != n_containers-1:
        con_fill_positions += list(range(cut_con_j+1, n_containers))
    con_fill_positions += list(range(cut_con_i+1))
    for pos in con_fill_positions:
        if child_CLS[pos] == 0:
            child_CLS[pos] = missing.pop(0)

    return {"BPS":child_BPS, "CLS":child_CLS}

def PerformCrossover(mating_pool, crossover_prob):
    # mating_pool = deepcopy(given_mating_pool)
    # crossover_prob = deepcopy(given_crossover_prob)
    next_population = []

    while len(mating_pool) > 0:
        if len(mating_pool) > 1:
            ind = random.sample(range(len(mating_pool)), 2)
            parent1 = mating_pool[ind[0]]
            parent2 = mating_pool[ind[1]]

            if random.random() < crossover_prob:
                child1 = CrossoverChromosomes(parent1, parent2)
                child2 = CrossoverChromosomes(parent2, parent1)
                next_population.extend([child1, child2])
            else:
                next_population.extend([parent1, parent2])

            for index in sorted(ind, reverse=True):
                del mating_pool[index]
        else:
            next_population.append(mating_pool.pop())

    return next_population

def plot_3d_objects(objects):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for idx, obj in enumerate(objects):
        x, y, z = obj.origin.tolist()
        l = obj.length
        w = obj.width
        h = obj.height
        
        # print(obj)
        
        # Define the vertices of the cuboid
        # vertices = [
        #     [x, y, z],  # bottom vertices
        #     [x + l, y, z],
        #     [x + l, y + w, z],
        #     [x, y + w, z],
        #     [x, y, z + h],  # top vertices
        #     [x + l, y, z + h],
        #     [x + l, y + w, z + h],
        #     [x, y + w, z + h]
        # ]
        
        vertices = [
            [x, y, z],  # bottom vertices
            [x + l, y, z],
            [x + l, y + h, z],
            [x, y + h, z],
            [x, y, z + w],  # top vertices
            [x + l, y, z + w],
            [x + l, y + h, z + w],
            [x, y + h, z + w]
        ]
        
        # Define the 6 faces of the cuboid
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
            [vertices[3], vertices[0], vertices[4], vertices[7]],  # left
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
            [vertices[4], vertices[5], vertices[6], vertices[7]]   # top
        ]
        # color = 'blue' if idx == 0 else 'blue'
        
        # Add the cuboid to the plot
        # ax.add_collection3d(Poly3DCollection(faces, alpha=0.5, edgecolor='k', facecolors=color))
    
        # Add the cuboid to the plot
        if idx!=0:
            ax.add_collection3d(Poly3DCollection(faces, alpha=0.5, edgecolor='k'))
            
        if idx==0:
            ax.add_collection3d(Poly3DCollection(faces, alpha=0.1, edgecolor='k', facecolors='red'))
    
    # Set labels and aspect
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    
    plt.show()
    
def PlotPackingSolution(packing_solution):
    # print("Packing solution: ", len(packing_solution))
    for container in packing_solution:
        if len(container) > 1:  # Ignore empty containers
            plot_3d_objects(container)
        else:
            print("Empty container")
            
def process_packing(packing_solution):
    ulds = {}
    packages = {}
    loading_sequence = []
    for idx, container in enumerate(packing_solution):
        if len(container) > 1:
            # ulds[f"ULD{idx+1}"] = container[0]
            # for i, package in enumerate(container[1:]):
            #     packages[f"Package{idx+1}_{i+1}"] = package
            x, z, y = container[0].origin.tolist()
            l = container[0].length
            w = container[0].width
            h = container[0].height
            ulds[f"ULD{idx+1}"] = ULD(length=l, height=h, width=w, uld_id=f"ULD{idx+1}", capacity=3000)
            for i, package in enumerate(container[1:]):
                x, z, y = package.origin.tolist()
                l = package.length
                w = package.width
                h = package.height
                packages[f"Package{idx+1}_{i+1}"] = Package(length=l, height=h, width=w, package_id=f"Package{idx+1}_{i+1}", priority="Priority", weight=1, delay=0)
                packages[f"Package{idx+1}_{i+1}"].generate_corners((x, y, z))
                packages[f"Package{idx+1}_{i+1}"].loaded = "ULD" + str(idx+1)
    return ulds, packages

class PackageMatcher:
    def __init__(self, packing_solution, uld_ids, package_ids):
        self.packing_solution = packing_solution
        uld_dimensions = []
        package_association = {}
        reverse_uld_ids, reverse_package_ids = {}, {}
        # reverse_uld_ids = {v: k for k, v in uld_ids.items()}
        # reverse_package_ids = {v: k for k, v in package_ids.items()}
        for k, v in uld_ids.items():
            if v not in reverse_uld_ids:
                reverse_uld_ids[v] = [k]
            else:
                reverse_uld_ids[v].append(k)
        for k, v in package_ids.items():
            # all permutations of length, width, height
            all_perm = [(v[0], v[1], v[2]), (v[0], v[2], v[1]), (v[1], v[0], v[2]), (v[1], v[2], v[0]), (v[2], v[0], v[1]), (v[2], v[1], v[0])]
            for perm in all_perm:
                if perm not in reverse_package_ids:
                    reverse_package_ids[perm] = [(k, perm)]
                else:
                    reverse_package_ids[perm].append((k, perm))
                
        marked_ulds = set()
        marked_packages = set()
        # print("Packing solution: ", (packing_solution))
        for idx, container in enumerate(packing_solution):
            if len(container) > 1:
                possible_uld_ids = reverse_uld_ids[(container[0].length, container[0].width, container[0].height)]
                uld_id = None
                for possible_uld_id in possible_uld_ids:
                    if possible_uld_id not in marked_ulds:
                        uld_id = possible_uld_id
                        marked_ulds.add(possible_uld_id)
                        break
                if uld_id is None:
                    raise Exception(f"No ULD found for container, container dimensions: {container[0].length, container[0].width, container[0].height}")
                
                for i, package in enumerate(container[1:]):
                    possible_package_ids = []
                    if (package.length, package.width, package.height) in reverse_package_ids:
                        possible_package_ids.extend(reverse_package_ids[(package.length, package.width, package.height)])
                    if (package.width, package.length, package.height) in reverse_package_ids:
                        possible_package_ids.extend(reverse_package_ids[(package.width, package.length, package.height)])
                    if (package.height, package.length, package.width) in reverse_package_ids:
                        possible_package_ids.extend(reverse_package_ids[(package.height, package.length, package.width)])
                    if (package.height, package.width, package.length) in reverse_package_ids:
                        possible_package_ids.extend(reverse_package_ids[(package.height, package.width, package.length)])
                    if (package.width, package.height, package.length) in reverse_package_ids:
                        possible_package_ids.extend(reverse_package_ids[(package.width, package.height, package.length)])
                    if (package.length, package.height, package.width) in reverse_package_ids:
                        possible_package_ids.extend(reverse_package_ids[(package.length, package.height, package.width)])
                
                    package_id = None
                    package_orientation = None
                    for possible_package_id in possible_package_ids:
                        if possible_package_id[0] not in marked_packages:
                            package_id = possible_package_id[0]
                            package_orientation = possible_package_id[1]    
                            marked_packages.add(possible_package_id)
                            break
                    if package_id is None:
                        raise Exception(f"No package found for container, container dimensions: {package.length, package.width, package.height}")
                    # orientation_matched_against = None
                    
                    
                    package_association[package_id] = uld_id, (package.origin.tolist()[0], package.origin.tolist()[2], package.origin.tolist()[1]), (package_orientation[0], package_orientation[1], package_orientation[2])
                    
        self.package_association = package_association
        
        # print(self.package_association)
        
    def get_parent_uld(self, package_id):
        return self.package_association[package_id][0]
    
    def get_package_position(self, package_id):
        return self.package_association[package_id][1]
    
    def get_package_orientation(self, package_id):
        return self.package_association[package_id][2]
    
    def is_placed(self, package_id):
        return package_id in self.package_association
                    

            

def PerformBoxPacking(containers,
                    boxes,
                    n_iter,
                    population_size,
                    elitism_size,
                    crossover_prob,
                    mutation_prob,
                    verbose=False,
                    plotSolution=False):

    if elitism_size < 0:
        raise Exception('Elitism size cant be negative')
    elif elitism_size == 0:
        print('Bad choice of elitism size')
    if len(containers) == 0:
        raise Exception('Specify containers')
    if len(boxes) == 0:
        raise Exception('Specify boxes')
    if n_iter <= 0:
        raise Exception('Number of iterations cant be <= 0')
    if population_size <= 0:
        raise Exception('Population size cant be <= 0')
    if crossover_prob < 0 or crossover_prob > 1:
        raise Exception('crossover_prob must be in [0;1]')
    elif crossover_prob == 0:
        print('Not the best choice for crossover_prob')
    if mutation_prob < 0 or mutation_prob > 1:
        raise Exception('mutation_prob must be in [0;1]')
    elif mutation_prob == 0:
        print('Not the best choice for mutation_prob')

    n = len(containers)
    m = len(boxes)

    population = InitializePopulation(population_size, n, boxes)
    chromosome_fitness = [0]*len(population)

    elitism_chromosomes = []
    elitism_chromosomes_fitness = []

    for iter_i in range(1, n_iter+1):
        # if verbose:
            # print('Iteration:', iter_i, 'out of', n_iter)

        for chrom_i in range(len(population)):
            # if verbose:
                # print('  Chromosome:', chrom_i+1, 'out of', len(population))
            chromosome = population[chrom_i]
            packing_solution = PackBoxes(boxes, containers, chromosome["BPS"], chromosome["CLS"])
            chromosome_fitness[chrom_i] = CalculateFitness(packing_solution)

        # Add elitism chromosomes
        population += elitism_chromosomes
        chromosome_fitness += elitism_chromosomes_fitness

        if iter_i != n_iter:
            # perform elitism
            best_chromosomes_ind = PerformElitism(chromosome_fitness, elitism_size)
            best_chromosomes_ind = list(best_chromosomes_ind)
            elitism_chromosomes = [population[i] for i in best_chromosomes_ind]
            elitism_chromosomes_fitness = [chromosome_fitness[i] for i in best_chromosomes_ind]

            # remove elitism from population
            remain_ind = [i for i in range(len(population)) if i not in best_chromosomes_ind]
            population = [population[i] for i in remain_ind]
            chromosome_fitness = [chromosome_fitness[i] for i in remain_ind]

            # selection
            mating_pool = PerformSelection(population, chromosome_fitness)

            # crossover
            crossovered_chromosomes = PerformCrossover(mating_pool, crossover_prob)

            # mutation
            population = PerformMutation(crossovered_chromosomes, mutation_prob)

    best_chromosome_index = np.argmin(chromosome_fitness)
    best_chromosome = population[best_chromosome_index]
    best_packing_solution = PackBoxes(boxes, containers, best_chromosome["BPS"], best_chromosome["CLS"])

    # PlotPackingSolution(best_packing_solution)
    
    return (best_packing_solution)


class ocm:
    def __init__(self, ulds, packages):
        self.ulds = ulds
        self.packages = packages


def get_packing_genetic_algorithm(container_dimensions, package_dimensions, n_iters=1, population_size=2):
    containers = [Container(length=c[0], width=c[1], height=c[2]) for c in container_dimensions]
    boxes = [Box(length=b[0], width=b[1], height=b[2]) for b in package_dimensions]
    
    

    best_packing_solution = PerformBoxPacking(containers=containers,   
                                        boxes=boxes,   
                                        n_iter=n_iters,   
                                        population_size=population_size,   
                                        elitism_size=5,   
                                        crossover_prob=0.5,   
                                        mutation_prob=0.5,   
                                        verbose=True,   
                                        plotSolution=True)

    # for package in packages:
    #     print(package, packages[package])
    # for uld in ulds:
    #     print(uld)
    
    uld_dimensions_dict = {}
    package_dimensions_dict = {}
    
    for uld in container_dimensions:
        uld_dimensions_dict[uld[3]] = (uld[0], uld[1], uld[2])
    for package in package_dimensions:
        package_dimensions_dict[package[3]] = (package[0], package[1], package[2])
    
    package_matcher = PackageMatcher(best_packing_solution, uld_dimensions_dict, package_dimensions_dict)

    return package_matcher

if __name__ == "__main__":
    # containers_np = np.loadtxt("R/uld.txt", skiprows=1) # adapt as needed
    containers_np = np.loadtxt("R/uld.txt", skiprows=1, dtype=object) # adapt as needed
    # containers = [Container(length=c[0], width=c[1], height=c[2]) for c in containers_data]
    containers_data = [[int(c[0]), int(c[1]), int(c[2]), str(c[3])] for c in containers_np]
    # packages_np = np.loadtxt("R/economic.txt", skiprows=1) # adapt as needed
    packages_np = np.loadtxt("R/economic.txt", skiprows=1, dtype=object) # adapt as needed
    # print(packages_np)
    packages_data = [[int(b[0]), int(b[1]), int(b[2]), str(b[3])] for b in packages_np]
    all_packages_id = [str(b[3]) for b in packages_data]
    # solution = PerformBoxPacking(containers=containers, boxes=packages, n_iter=2, population_size=10, elitism_size=5, crossover_prob=0.5, mutation_prob=0.5, verbose=True, plotSolution=True)
    
    # ocm_solution = process_packing(solution)
    package_matcher = get_packing_genetic_algorithm(containers_data, packages_data)
    
    for package_id in all_packages_id:
        print(package_matcher.get_package_position(package_id), package_matcher.get_parent_uld(package_id))
    
    # sv = SolutionValidator(ocm_solution)
    # sv.validate()
    # print(sv.is_valid())
    # print(sv.priority_score())
    # print(sv.economy_score())
    
    
