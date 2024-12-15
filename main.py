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
    GREEDY_ITERATIONS = 2
    
    costs = []
    matplotlib.pyplot.close("all")
    
    random_seed = 28072
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    
    runs_ocm_cost = {}
    
    ulds, packages, K = parse_input(input_file)
    ga_ocm = OptimalCargoManagement(ulds, packages, K, verbose)
    ga_ocm.create_package_ordering()
    ga_ocm.run_genetic_algorithm()
    ga_ocm.adhoc_additions()
    
    ga_sv = SolutionValidator(ga_ocm, verbose)
    ga_sv.validate()
    if ga_sv.is_valid():
        print("GA solution is valid.")
        print("GA solution cost: ", ga_ocm.cost())  
    else:
        print("GA solution is invalid.")
        ga_ocm = None   
        
    greedy_ocm_list = []
    for i in range(GREEDY_ITERATIONS):
        greedy_ulds, greedy_packages, K = parse_input(input_file)
        greedy_ocm = OptimalCargoManagement(greedy_ulds, greedy_packages, K, verbose)
        greedy_priority_ordering, greedy_economy_ordering = greedy_ocm.create_package_ordering()
        greedy_ocm.reorient_packages()
        
        for top_k in range(min(greedy_ocm.MIN_PRIORITY_ULDS, len(greedy_ocm.ulds)//2) + 1, len(greedy_ocm.ulds)+1):
            largest_ulds_by_volume = sorted(
                        greedy_ocm.ulds.keys(),
                        key=lambda x: ((greedy_ocm.ulds[x].length * greedy_ocm.ulds[x].width * greedy_ocm.ulds[x].height),x),
                        reverse=True
                    )[:top_k]
                
            greedy_ocm.fit_greedy(optional_ordering=greedy_priority_ordering, selected_ulds=largest_ulds_by_volume)
            unused_ulds = greedy_ocm.unused_uld_ids()
            greedy_ocm.fit_greedy(optional_ordering=greedy_economy_ordering, selected_ulds=unused_ulds)
            greedy_ocm.adhoc_additions()
            sv = SolutionValidator(greedy_ocm, verbose)
            sv.validate()
            if sv.is_valid():
                print(f"Greedy solution {i} is valid.")
                greedy_ocm_list.append(greedy_ocm)
                break
            
    min_greedy_cost, min_greedy_cost_arg = min([ocm.cost() for ocm in greedy_ocm_list]), np.argmin([ocm.cost() for ocm in greedy_ocm_list])
    min_greedy_ocm = greedy_ocm_list[min_greedy_cost_arg]

    final_ocm_solution = ga_ocm if ga_ocm.cost() < min_greedy_cost else min_greedy_ocm
    final_sv = SolutionValidator(final_ocm_solution, verbose)
    final_sv.validate()
    if final_sv.is_valid():
        print("Final solution is valid.")
    else:
        print("Final solution is invalid.")
        final_ocm_solution = None
    final_ocm_solution.file_output_ocm(output_file)
    print("Minimum Greedy Solution Cost: ", min_greedy_cost)
    visualize(input_file=input_file, output_file=output_file, show = False)