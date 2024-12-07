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
    verbose = True if sys.argv[3] == "1" else False
    
    costs = []
    matplotlib.pyplot.close("all")
    
    random_seed = 28072
    print("Random seed:", random_seed)
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    runs_ocm_cost = {}
    
    def run_simulation(run_number):
        ulds, packages, K = parse_input(input_file)
        ocm = OptimalCargoManagement(ulds, packages, K, verbose)
        ocm.create_package_ordering()
        ocm.run_genetic_algorithm()
        ocm.adhoc_additions()
        print(run_number, ocm.cost())
        return ocm
    
    all_ocms = []
    ocm = run_simulation(1)
    sv = SolutionValidator(ocm, verbose)
    sv.validate()
    if sv.is_valid():
        all_ocms.append(ocm)
    else:
        print(f"Invalid solution for run {0 + 1}")

    costs = [ocm.cost() for ocm in all_ocms]
    
    min_cost_arg, min_cost = np.argmin(costs), min(costs)
    if verbose:
        print(f"Minimum cost: {min_cost}")
    min_ocm = all_ocms[min_cost_arg]
    min_ocm.file_output_ocm(f"{output_file}")
        
    visualize(input_file=input_file, output_file=output_file, show = False)