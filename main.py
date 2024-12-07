from uld import ULD
from package import Package, crainic_sorting 
from visualizer import visualize
import random
import matplotlib.pyplot
from io_utils import parse_input
from ocm import OptimalCargoManagement
from ga import get_packing_genetic_algorithm 
from validator import SolutionValidator 
import numpy as np

from threading import Thread


if __name__ == "__main__":
    costs = []
    matplotlib.pyplot.close("all")

    
    runs_ocm_cost = {}
    
    def run_simulation(random_run):
        
        random_seed = random.randint(0, 100000)
        print("Random seed:", random_seed)
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        ulds, packages, K = parse_input("data/Challenge_FedEx.txt")
        
        show = False
        output_file = f"solution_{random_run}.txt"
        ocm = OptimalCargoManagement(ulds, packages, K)
        priority_ordering, non_priority_ordering = ocm.create_package_ordering()
        
        containers_data = []
        packages_data = []
        
        for uld_id, uld in ocm.ulds.items():
            if uld_id in ['U4', 'U5', 'U6']:
                containers_data.append([uld.length, uld.width, uld.height, uld.uld_id])
            
        for package_id, package in ocm.packages.items():
            if package.priority:
                packages_data.append([package.length, package.width, package.height, package.package_id])
                
        ga_solution = get_packing_genetic_algorithm(containers_data, packages_data)
                
        for package_id, package in ocm.packages.items():
            if package.priority:
                parent_uld = ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = ga_solution.get_package_orientation(package_id=package.package_id)
                
                package.loaded = parent_uld
                package.length, package.width, package.height = pkg_orientation[0], pkg_orientation[1], pkg_orientation[2]
                package.generate_corners(ref_corner)
                
        unused_uld_ids = ocm.unused_uld_ids()
        
        for uld_id, uld in ocm.ulds.items():
            if uld_id in unused_uld_ids:
                uld.refresh()
        
        non_priority_delay_dict = {}
        non_priority_volume_dict = {}
        
        for package_id, package in ocm.packages.items():
            if not package.priority:
                non_priority_delay_dict[package.package_id] = package.delay
                non_priority_volume_dict[package.package_id] = package.length * package.width * package.height
                
        actual_pkgs = non_priority_ordering
        actual_pkgs.sort(key=lambda x: (non_priority_delay_dict[x[0]]) ** 1 / (non_priority_volume_dict[x[0]]) ** 1.2, reverse=True)
        actual_pkgs = actual_pkgs[:150]
        actual_pkgs = [x[0] for x in actual_pkgs]
        
        random.shuffle(actual_pkgs)
        
        eco_containers_data = []
        eco_packages_data = []
        
        for uld_id, uld in ocm.ulds.items():
            if uld_id in unused_uld_ids:
                eco_containers_data.append([uld.length, uld.width, uld.height, uld.uld_id])
            
        for package_id, package in ocm.packages.items():
            if not package.priority and package.package_id in actual_pkgs:
                eco_packages_data.append([package.length, package.width, package.height, package.package_id])
        
        eco_ga_solution = get_packing_genetic_algorithm(eco_containers_data, eco_packages_data)
        
        for package_id, package in ocm.packages.items():
            if not package.priority and package.package_id in actual_pkgs:
                if not eco_ga_solution.is_placed(package_id=package.package_id):
                    continue
                parent_uld = eco_ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = eco_ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = eco_ga_solution.get_package_orientation(package_id=package.package_id)
                
                package.loaded = parent_uld
                package.length, package.width, package.height = pkg_orientation[0], pkg_orientation[1], pkg_orientation[2]
                package.generate_corners(ref_corner)
        
        for package_id, package in ocm.packages.items():
            if package.loaded:
                ocm.ulds[package.loaded].add_package(package)
        
        ocm.adhoc_additions()
        
        print(random_run + 1, ocm.cost())
        
        return ocm
    
    all_ocms = []
    
    for random_run in range(10):
        print("Running simulation", random_run + 1)
        ocm = run_simulation(random_run)
        sv = SolutionValidator(ocm)
        sv.validate()
        if sv.is_valid():
            all_ocms.append(ocm)
        else:
            print(f"Invalid solution for run {random_run + 1}")

    costs = [ocm.cost() for ocm in all_ocms]
    
    min_cost_arg, min_cost = np.argmin(costs), min(costs)
    print(f"Minimum cost: {min_cost} at run {min_cost_arg + 1}")
    min_ocm = all_ocms[min_cost_arg]
    output_file = f"solution_best.txt"
    min_ocm.file_output_ocm(f"output/{output_file}")
        
    visualize("data/Challenge_FedEx.txt", output_file, show = True)