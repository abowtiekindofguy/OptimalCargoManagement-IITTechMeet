from uld import ULD
from package import Package, crainic_sorting 
from visualizer import visualize
import random
import matplotlib.pyplot

class OptimalCargoManagement(object):
    def __init__(self, ulds, packages, K):
        self.ulds = ulds
        self.packages = packages
        self.K = K
        self.package_ordering = []
        # self.create_package_ordering()
        
    def add_uld(self, uld):
        self.ulds[uld.uld_id] = uld 
        
    def add_package(self, package):
        self.packages[package.package_id] = package
        
    def cost(self, only_priority = False):
        total_cost = 0
        priority_activated_ulds = set()
        for package_id, package in self.packages.items():
            if package.loaded is not None and package.priority:
                priority_activated_ulds.add(package.loaded)
        priority_cost = len(priority_activated_ulds) * self.K
        economy_cost = 0
        for package_id, package in self.packages.items():
            if not package.priority and package.loaded is None:
                economy_cost += package.delay
        total_cost = priority_cost + economy_cost
        # print(f"Priority cost: {priority_cost}, Economy cost: {economy_cost}, Total cost: {total_cost}")
        if only_priority:
            return priority_cost
        else:
            return total_cost
    
    def fit(self, optional_ordering = None, selected_ulds = None):
        # print(self.package_ordering)
        # print(len(self.package_ordering))
        if optional_ordering is not None:
            for order in optional_ordering:
                package_id = order[0]
                if selected_ulds is not None:
                    for uld_id in selected_ulds:
                        r = self.ulds[uld_id].update_filled_coordinates(self.packages[package_id])
                        if r: break
                else:
                    # for uld_id, uld in self.ulds.items():
                    #     r = uld.fit_in_package(self.packages[package_id])
                    #     if r: break
                    for uld_id, uld in self.ulds.items():
                        r = uld.update_filled_coordinates(self.packages[package_id])
                        if r: break
        else:
            for order in self.package_ordering:
                package_id = order[0]
                for uld_id, uld in self.ulds.items():
                    r = uld.update_filled_coordinates(self.packages[package_id])
                    if r: break
        
                    
    def __repr__(self):
        package_string = "\n"
        for package_id, package in self.packages.items():
            if package.loaded is not None:
                package_string += f"{package}\n"
        # return f"OptimalCargoManagement({self.ulds}, {self.packages}, {self.K}) + {package_string}"
        return package_string
    
    
    def print_solution(self, filename):
        with open(filename, 'w') as file:
            file.write("9,9,9\n")
            for package_id, package in self.packages.items():
                if package.loaded is not None:
                    file.write(f"{package.package_id},{package.loaded},{package.corners[0][0]},{package.corners[0][1]},{package.corners[0][2]},{package.corners[7][0]},{package.corners[7][1]},{package.corners[7][2]}\n")

    
    def create_package_ordering(self):
        priority_packages_dict = {}
        non_priority_packages_dict = {}
        for package_id, package in self.packages.items():
            if package.priority:
                priority_packages_dict[package_id] = package
            else:
                non_priority_packages_dict[package_id] = package
                
            
        priority_ordering = crainic_sorting(priority_packages_dict, group_on_dim = True, opposite_order = True)
        non_priority_ordering = crainic_sorting(non_priority_packages_dict, group_on_dim = True)
        self.package_ordering = priority_ordering + non_priority_ordering
        return priority_ordering, non_priority_ordering
        
        
    def reorient_packages(self):
        for order in self.package_ordering:
            package_id = order[0]
            order_z_against = order[1]            
            package_to_reorient = self.packages[package_id]
            package_to_reorient.reorient(order_z_against)
            
    def extra_additions(self):
        for uld_id, uld in self.ulds.items():
            uld.create_cuboid_environment()
        extra_count = 0
        unloaded_pkd_ids = []
        for package_id, package in self.packages.items():
            if package.loaded is None:
                unloaded_pkd_ids.append(package_id)
        # random.shuffle(unloaded_pkd_ids)
        sorted_unloaded_pkd_ids = sorted(unloaded_pkd_ids, key = lambda x: self.packages[x].delay, reverse = True)
        # for package_id, package in self.packages.items():
            # print(package_id)
        for package_id in sorted_unloaded_pkd_ids:
            package = self.packages[package_id]
            if extra_count > 450:
                break
            if package.loaded is None:
                print(f"Package {package_id} not loaded")
                for uld_id, uld in self.ulds.items():
                    r = uld.fit_in_package(package)
                    print(r)
                    extra_count += 1
                    if r: break
                print(package)
                
                
    def print_packing_efficiency(self):
        volume_filled = {}
        volume_original = {}
        weight_filled = {}
        weight_original = {}
        for uld_id, uld in self.ulds.items():
            volume_filled[uld_id] = 0
            weight_filled[uld_id] = 0
            volume_original[uld_id] = uld.length * uld.width * uld.height
            weight_original[uld_id] = uld.capacity
        for package_id, package in self.packages.items():
            if package.loaded is not None:
                volume_filled[package.loaded] += package.length * package.width * package.height
                weight_filled[package.loaded] += package.weight
        for uld_id, uld in self.ulds.items():
            print(f"{uld_id} Volume: {volume_filled[uld_id]/volume_original[uld_id]} Weight: {weight_filled[uld_id]/weight_original[uld_id]}")
    
    def shift_priority_packages(self):
        # uld_priority_count = {}
        # for package_id, package in self.packages.items():
        #     if package.loaded is not None and package.priority:
        #         if package.loaded in uld_priority_count:
        #             uld_priority_count[package.loaded] += 1
        #         else:
        #             uld_priority_count[package.loaded] = 1
        # print(f"ULD priority count: {uld_priority_count}")  
        # #lowest priority uld
        # # zero_priority_count_uld = min(uld_priority_count, key = uld_priority_count.get)
        # all_ulds = set(self.ulds.keys())
        # lowest_priority_count_uld = min(uld_priority_count, key = uld_priority_count.get)
        # zero_priority_count_uld = all_ulds - set(uld_priority_count.keys())
        # zero_priority_count_uld = list(zero_priority_count_uld)[0]
        # priority_packages_in_lowest_priority_uld = []
        # for package_id, package in self.packages.items():
        #     if package.loaded == lowest_priority_count_uld and package.priority:
        #         priority_packages_in_lowest_priority_uld.append(package)
        # print(f"Priority packages in lowest priority uld: {len(priority_packages_in_lowest_priority_uld)}")
        # print(f"{priority_packages_in_lowest_priority_uld}")
        # print(lowest_priority_count_uld, zero_priority_count_uld)
        unmatched_packages = []
        filled_ulds = []
        uld_occupancy = {}
        for package_id, package in self.packages.items():
            if package.loaded is None and package.priority:
                unmatched_packages.append(package)
            elif package.loaded is not None:
                filled_ulds.append(package.loaded)
                if package.loaded in uld_occupancy:
                    uld_occupancy[package.loaded] += 1
                else:
                    uld_occupancy[package.loaded] = 1
                
        print(f"Filled ulds: {uld_occupancy}")
        print("Priority packages not loaded: ", len(unmatched_packages))
        filled_ulds.sort(reverse=True)
        for uld_id, uld in self.ulds.items():
            if uld_id in filled_ulds:
                uld.create_cuboid_environment()
        packages_shifted = 0
        for package in unmatched_packages:
            package.loaded = None
            # self.ulds[lowest_priority_count_uld].remove_package(package)
            for uld_id, uld in self.ulds.items():
                if uld_id in filled_ulds:
                    r = uld.fit_in_package(package)
                    if r:
                        print(f"Package {package.package_id} shifted to {uld_id}")
                        # self.print_packing_efficiency()
                        # uld_priority_count[uld_id] += 1
                        packages_shifted += 1
                        break
            if package.loaded is None:
                print("Total packages shifted: ", packages_shifted)
                print(f"Package {package.package_id} not shifted")
                self.print_packing_efficiency()
                return False
        return True      
                
                
    def unused_uld_ids(self):
        package_uld_count = {}
        for package_id, package in self.packages.items():
            if package.loaded in package_uld_count:
                package_uld_count[package.loaded] += 1
            else:
                package_uld_count[package.loaded] = 1
        unused_uld_ids = []
        for uld_id, uld in self.ulds.items():
            if uld_id not in package_uld_count:
                unused_uld_ids.append(uld_id)
                
        return unused_uld_ids
        
        
    
    
def parse_input(file):
    with open(file, 'r') as file:
        lines = file.readlines()
    uld_count = int(lines[0]) 
    ulds = {}
    line_index = 1
    for _ in range(uld_count):
        uld_data = lines[line_index].split(",")
        uld_id=uld_data[0]
        length=uld_data[1]
        width=uld_data[2]
        height=uld_data[3]
        capacity=uld_data[4]
        ulds[uld_id] = ULD(uld_id, int(length), int(width), int(height), int(capacity))
        line_index += 1

    package_count = int(lines[line_index]) 
    packages = {}
    line_index += 1
    for _ in range(package_count):
        package_data = lines[line_index].split(",")
        package_id, length, width, height, weight, priority, delay = package_data
        priority = priority.strip()
        weight = int(weight)
        delay = delay
        packages[package_id] = Package(package_id, int(length), int(width), int(height), weight, priority, delay)
        line_index += 1

    K = int(lines[line_index]) 

    return ulds, packages, K

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
        ocm.fit(optional_ordering=priority_ordering, selected_ulds=['U6','U5','U4'])    
        cost_priority = ocm.cost(only_priority=True)
        bb = False
        # if cost_priority < 30000:
        #     # ocm.extra_additions()
        ocm.print_packing_efficiency()
        
        bb = ocm.shift_priority_packages()
        # ocm.print_packing_efficiency()
        
        show = True
        if ocm.cost(only_priority=True) >= 25000 or not bb:
            continue
        # print(ocm.cost())
        unused_uld_ids = ocm.unused_uld_ids()
        for uld_id, uld in ocm.ulds.items():
            if uld_id in unused_uld_ids:
                uld.refresh()
        ocm.fit(optional_ordering=non_priority_ordering, selected_ulds=unused_uld_ids)
        print(ocm.cost())
        
        ocm.extra_additions()
        print(ocm.cost())

        print(random_run+1, ocm.cost())
        costs.append(ocm.cost())
        ocm.print_solution(f"output/{output_file}")
        visualize("data/Challenge_FedEx.txt", output_file, show = show)
        break
        
    # print(min(costs))
    # print(costs.index(min(costs)))  