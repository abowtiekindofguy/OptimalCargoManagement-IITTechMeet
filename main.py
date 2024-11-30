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
        
    def cost(self):
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
        print(f"Priority cost: {priority_cost}, Economy cost: {economy_cost}, Total cost: {total_cost}")
        return total_cost
    
    def fit(self):
        # print(self.package_ordering)
        # print(len(self.package_ordering))
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
        priority_ordering = crainic_sorting(priority_packages_dict, group_on_dim = True, opposite_order = False)
        non_priority_ordering = crainic_sorting(non_priority_packages_dict, group_on_dim = True)
        self.package_ordering = priority_ordering + non_priority_ordering
        
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
    for random_run in range(50):
        show = False
        ulds, packages, K = parse_input("data/Challenge_FedEx.txt")
        output_file = f"solution_{random_run}.txt"
        ocm = OptimalCargoManagement(ulds, packages, K)
        ocm.create_package_ordering()
        ocm.reorient_packages()
        ocm.fit()
        cost_before = ocm.cost()
        if cost_before < 50000:
            ocm.extra_additions()
            show = True
        print(random_run+1, ocm.cost())
        costs.append(ocm.cost())
        ocm.print_solution(f"output/{output_file}")
        visualize("data/Challenge_FedEx.txt", output_file, show = show)
        
    print(min(costs))
    print(costs.index(min(costs)))  