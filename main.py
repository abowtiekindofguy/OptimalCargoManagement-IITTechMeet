from visualizer import visualize
import random
import matplotlib
from io_utils import parse_input
from ocm import OptimalCargoManagement
from validator import SolutionValidator 
import numpy as np
import sys

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    verbose = sys.argv[3]
    
    costs = []
    matplotlib.pyplot.close("all")
    
    random_seed = 28072
    print("Random seed:", random_seed)
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    runs_ocm_cost = {}
    
    def run_simulation(run_number):
        ulds, packages, K = parse_input(input_file)

        ocm = OptimalCargoManagement(ulds, packages, K)
        
        ocm.create_package_ordering()
        
        ocm.run_genetic_algorithm()
        
        ocm.adhoc_additions()
        
        print(run_number + 1, ocm.cost())
        
        return ocm
    
    all_ocms = []
    
    for run_number in range(1):
        print("Running simulation", run_number + 1)
        ocm = run_simulation(run_number)
        sv = SolutionValidator(ocm)
        sv.validate()
        if sv.is_valid():
            all_ocms.append(ocm)
        else:
            print(f"Invalid solution for run {run_number + 1}")

    costs = [ocm.cost() for ocm in all_ocms]
    
    min_cost_arg, min_cost = np.argmin(costs), min(costs)
    print(f"Minimum cost: {min_cost} at run {min_cost_arg + 1}")
    min_ocm = all_ocms[min_cost_arg]
    output_file = f"solution.txt"
    min_ocm.file_output_ocm(f"{output_file}")
        
    visualize(input_file=input_file, output_file=output_file, show = True)