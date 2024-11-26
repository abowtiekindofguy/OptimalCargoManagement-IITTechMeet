from uld import ULD
from package import Package 

class OptimalCargoManagement(object):
    def __init__(self, ulds, packages, K):
        self.ulds = ulds
        self.packages = packages
        self.K = K
        
    def add_uld(self, uld):
        self.ulds[uld.uld_id] = uld 
        
    def add_package(self, package):
        self.packages[package.package_id] = package
        
    def cost(self):
        total_cost = 0
        for uld_id, uld in self.ulds.items():
            total_cost += uld.cost(self.K)
        for package_id, package in self.packages.items():
            if package.loaded is None: total_cost += package.delay
            
        return total_cost
    
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
    ulds, packages, K = parse_input("input.txt")
    ocm = OptimalCargoManagement(ulds, packages, K)
    print(ocm.cost())