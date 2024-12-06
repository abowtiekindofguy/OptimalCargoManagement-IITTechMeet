## Solution Validator
from package import Package
from uld import ULD
from cuboid import Cuboid

def validate_uld(uld, packages):
    uld_cuboid = Cuboid((0,0,0), (uld.length, uld.width, uld.height))
    package_cuboid_list = []
    for package in packages:
        package_cuboid = Cuboid(package.corners[0], package.corners[7])
        package_cuboid_list.append(package_cuboid)
    for i in range(len(package_cuboid_list)):
        if not package_cuboid_list[i].fits_inside(uld_cuboid):
            return False
        for j in range(i+1, len(package_cuboid_list)):
            if package_cuboid_list[i].intersects(package_cuboid_list[j]):
                return False
            
    return True

class SolutionValidator:
    def __init__(self, solution):
        self.solution_packages = solution.packages
        self.solution_ulds = solution.uld
        self.valid = False
        self.package_collection = None

    def validate(self):
        package_collection = {uld_id:[] for uld_id in self.solution_ulds}
        self.package_collection = package_collection    
        for package_id, package in self.solution_packages.items():
            if package.loaded:
                package_collection[package.loaded].append(package)
                
        for uld_id in package_collection:
            uld = self.solution_ulds[uld_id]
            validate_uld = validate_uld(uld, package_collection[uld_id])
            if not validate_uld:
                self.valid = False
                return
            
        self.valid = True
        return
        
    def is_valid(self):
        return self.valid
    
    def priority_score(self):
        assert self.valid, "Solution is not valid"
        assert self.package_collection is not None, "Solution is not validated"
        
        priority_score = 0
        
        for uld_id in self.package_collection:
            uld_priority_score = 0  
            for package in self.package_collection[uld_id]:
                if package.priority:
                    uld_priority_score = 1
                    break
            priority_score += uld_priority_score
            
        return priority_score
    
    def economy_score(self):
        assert self.valid, "Solution is not valid"
        assert self.package_collection is not None, "Solution is not validated"
        
        delay_score = 0
        
        for package in self.solution_packages.values():
            if package.loaded is None:
                delay_score += package.delay
            
        return delay_score
    
    def total_score(self):
        assert self.valid, "Solution is not valid"
        assert self.package_collection is not None, "Solution is not validated"
        
        economy_score, priority_score = self.economy_score(), self.priority_score() 
        
        return economy_score + priority_score
    
    