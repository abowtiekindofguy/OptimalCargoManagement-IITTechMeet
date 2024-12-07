from uld import ULD
from package import Package, crainic_sorting 
from visualizer import visualize
import random
import matplotlib.pyplot
from io_utils import parse_input
from ocm import OptimalCargoManagement
from ga import get_packing_genetic_algorithm 
from validator import SolutionValidator 

if __name__ == "__main__":
    costs = []
    matplotlib.pyplot.close("all")
    for random_run in range(500):
        show = False
        ulds, packages, K = parse_input("data/Challenge_FedEx.txt")
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
        
        # ga_solution_parent = ga_solution.get_parent_uld()
        # ga_solution_position = ga_solution.get_package_position()
        
        # for package_id, package in packages.items():
        #     if package.id in ga_solution_position:
                
        for package_id, package in ocm.packages.items():
            if package.priority:
                parent_uld = ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = ga_solution.get_package_orientation(package_id=package.package_id)
                
                package.loaded = parent_uld
                # package.generate_corners(ref_corner, pkg_orientation)
                package.length, package.width, package.height = pkg_orientation[0], pkg_orientation[1], pkg_orientation[2]
                package.generate_corners(ref_corner)
                
                print(package)  
                
        
            
        print(ocm.cost())
        unused_uld_ids = ocm.unused_uld_ids()
        
        print(unused_uld_ids)
        
        for uld_id, uld in ocm.ulds.items():
            if uld_id in unused_uld_ids:
                uld.refresh()
        # ocm.fit(optional_ordering=non_priority_ordering, selected_ulds=['U3','U2','U1'])  
        
        non_priority_delay_dict = {}
        non_priority_volume_dict = {}
        
        for package_id, package in ocm.packages.items():
            if not package.priority:
                non_priority_delay_dict[package.package_id] = package.delay
                non_priority_volume_dict[package.package_id] = package.length*package.width*package.height
                
        # non_priority_sorted_by_delay_rev = [k for k, v in sorted(non_priority_delay_dict.items(), key=lambda item: item[1], reverse=True)]
        actual_pkgs = non_priority_ordering
        actual_pkgs.sort(key = lambda x: (non_priority_delay_dict[x[0]])**1/(non_priority_volume_dict[x[0]])**1.2, reverse = True)
        # actual_pkgs.sort(key = lambda x: non_priority_volume_dict[x[0]], reverse = False)
        # power 1- 123 30745, 1.1 - 30512, 1.2 - 30440
        actual_pkgs = actual_pkgs[:150]
        actual_pkgs = [x[0] for x in actual_pkgs]
        
        random.shuffle(actual_pkgs)
        
        print(len(actual_pkgs))        
        
        
        # print(actual_pkgs)
        
        
        eco_containers_data = []
        eco_packages_data = []
        
        for uld_id, uld in ocm.ulds.items():
            if uld_id in unused_uld_ids:
                eco_containers_data.append([uld.length, uld.width, uld.height, uld.uld_id])
            
        for package_id, package in ocm.packages.items():
            if not package.priority and package.package_id in actual_pkgs:
                eco_packages_data.append([package.length, package.width, package.height, package.package_id])
                
        print(eco_containers_data, eco_packages_data)
        
        eco_ga_solution = get_packing_genetic_algorithm(eco_containers_data, eco_packages_data)
        
                
        for package_id, package in ocm.packages.items():
            if not package.priority and package.package_id in actual_pkgs:
                if not eco_ga_solution.is_placed(package_id=package.package_id):
                    continue
                parent_uld = eco_ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = eco_ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = eco_ga_solution.get_package_orientation(package_id=package.package_id)
                
                package.loaded = parent_uld
                # package.generate_corners(ref_corner, pkg_orientation)
                package.length, package.width, package.height = pkg_orientation[0], pkg_orientation[1], pkg_orientation[2]
                package.generate_corners(ref_corner)
                
                print(package)  
        
        for package_id, package in ocm.packages.items():
            if package.loaded:
                ocm.ulds[package.loaded].add_package(package)
        
        
        ocm.extra_additions()
        print("Hi1")
        ocm.extra_additions()
        print("Hi2")
        ocm.extra_additions()
        print("Hi3")
        ocm.extra_additions()
        
        
        # print(ocm.cost())
        
        print(random_run+1, ocm.cost())
        costs.append(ocm.cost())
        ocm.print_solution(f"output/{output_file}")
        
        sv = SolutionValidator(ocm)
        sv.validate()
        print(sv.economy_score())
        print(sv.priority_score())
        
        
        visualize("data/Challenge_FedEx.txt", output_file, show = True)
        
        
        
        
        
        
        
        
        
        
        # ocm.reorient_packages()
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
        # ocm.fit(optional_ordering=non_priority_ordering, selected_ulds=['U3','U2','U1'])
        
        
        
        # print(ocm.cost())
        
        # ocm.extra_additions()
        # print(ocm.cost())

        # print(random_run+1, ocm.cost())
        # costs.append(ocm.cost())
        # ocm.print_solution(f"output/{output_file}")
        # visualize("data/Challenge_FedEx.txt", output_file, show = True)
        # break
        # ocm_solution = get_packing_genetic_algorithm(containers_data, packages_data)
        # sv = SolutionValidator(ocm_solution)
        # sv.validate()
        # print(sv.is_valid())
        # print(sv.priority_score())
        # print(sv.economy_score())
        
    # print(min(costs))
    # print(costs.index(min(costs)))  