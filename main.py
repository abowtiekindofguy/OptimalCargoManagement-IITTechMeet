from uld import ULD
from package import Package, crainic_sorting 
from visualizer import visualize
import random
import matplotlib.pyplot
from io_utils import parse_input
from ocm import OptimalCargoManagement

if __name__ == "__main__":
    costs = []
    matplotlib.pyplot.close("all")
    for random_run in range(500):
        show = False
        ulds, packages, K = parse_input("data/Challenge_FedEx.txt")
        output_file = f"solution_{random_run}.txt"
        ocm = OptimalCargoManagement(ulds, packages, K)
        priority_ordering, non_priority_ordering = ocm.create_package_ordering()
        ocm.reorient_packages()
        #fit priority packages first
        # ocm.fit(optional_ordering=priority_ordering, selected_ulds=['U6', 'U5', 'U4', 'U3', 'U2', 'U1'])
        # cost_priority = ocm.cost(only_priority=True)
        # bb = False
        # if cost_priority < 30000:
        #     # ocm.extra_additions()
        #     bb = ocm.shift_priority_packages()
            
        #     show = True
            
        # # bb = ocm.shift_priority_packages()
        # if ocm.cost(only_priority=True) >= 25000 or not bb:
        #     continue
        # print(ocm.cost())
        # unused_uld_ids = ocm.unused_uld_ids()
        
        # for uld_id, uld in ocm.ulds.items():
        #     if uld_id in unused_uld_ids:
        #         uld.refresh()
        ocm.fit(optional_ordering=non_priority_ordering, selected_ulds=['U3','U2','U1'])
        
        
        
        # print(ocm.cost())
        
        ocm.extra_additions()
        # print(ocm.cost())

        print(random_run+1, ocm.cost())
        costs.append(ocm.cost())
        ocm.print_solution(f"output/{output_file}")
        visualize("data/Challenge_FedEx.txt", output_file, show = True)
        break
        
    # print(min(costs))
    # print(costs.index(min(costs)))  