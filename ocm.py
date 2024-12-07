import random   
from package import crainic_sorting

class OptimalCargoManagement(object):
    def __init__(self, ulds, packages, K, verbose = False):
        self.ulds = ulds
        self.packages = packages
        self.K = K
        self.package_ordering = []
        self.verbose = verbose
        # self.create_package_ordering()
        
    def log(self, message):
        if self.verbose: print(message)
        
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
        self.log(f"Priority cost: {priority_cost}, Economy cost: {economy_cost}, Total cost: {total_cost}")
        if only_priority: return priority_cost
        else: return total_cost
    
    def fit(self, optional_ordering = None, selected_ulds = None):
        # print(self.package_ordering)
        # print(len(self.package_ordering))
        self.log(f"Fitting packages: {len(self.packages)} packages in {len(self.ulds)} ULDs")
        self.log(f"Optional ordering: {True if optional_ordering is not None else False}")   
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
        uld_string = "Loaded ULDs:\n"
        for uld_id, uld in self.ulds.items():
            if uld.filled_coordinates:
                uld_string += f"{uld}\n"
        package_string = "Loaded Packages:\n"
        for package_id, package in self.packages.items():
            if package.loaded is not None:
                package_string += f"{package}\n"
        package_string += "Unloaded Packages:\n"
        for package_id, package in self.packages.items():
            if package.loaded is None:
                package_string += f"{package}\n"
        # return f"OptimalCargoManagement({self.ulds}, {self.packages}, {self.K}) + {package_string}"
        # return package_string
        ocm_attributes = f"OptimalCargoManagement Attributes = {len(self.ulds)} ULDs, {len(self.packages)} Packages, K = {self.K}"   
        return uld_string + package_string + ocm_attributes
    
    def print_solution(self, filename):
        with open(filename, 'w') as file:
            file.write("9,9,9\n")
            
            for package_id, package in self.packages.items():
                if package.loaded is not None:
                    file.write(f"{package.package_id},{package.loaded},{package.corners[0][0]},{package.corners[0][1]},{package.corners[0][2]},{package.corners[7][0]},{package.corners[7][1]},{package.corners[7][2]}\n")
                else:
                    file.write(f"{package.package_id},NONE,-1,-1,-1,-1,-1,-1\n")
    
    def create_package_ordering(self):
        priority_packages_list = [package for package in self.packages.values() if package.priority]
        non_priority_packages_list = [package for package in self.packages.values() if not package.priority]

            
        priority_ordering = crainic_sorting(packages_list = priority_packages_list, group_on_dimensions= True, reverse = False)
        non_priority_ordering = crainic_sorting(packages_list = non_priority_packages_list, group_on_dimensions=True)
        
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
            # print(f"ULD {uld_id} creating cuboid environment")
            uld.create_cuboid_environment()
        extra_count = 0
        unloaded_pkd_ids = []
        for package_id, package in self.packages.items():
            if package.loaded is None:
                unloaded_pkd_ids.append(package_id)
        # random.shuffle(unloaded_pkd_ids)
        sorted_unloaded_pkd_ids = sorted(unloaded_pkd_ids, key = lambda x: self.packages[x].delay/(max([self.packages[x].height,self.packages[x].width,self.packages[x].length])), reverse = True)
        # for package_id, package in self.packages.items():
            # print(package_id)
        num_unloaded = len(sorted_unloaded_pkd_ids)
        for package_id in sorted_unloaded_pkd_ids:
            package = self.packages[package_id]
            # if extra_count > 450:
            #     break
            if package.loaded is None:
                # print(f"Package {package_id} not loaded")
                for uld_id, uld in self.ulds.items():
                    # print("Trying to load in ULD", uld_id)
                    r = uld.fit_in_package(package)
                    # print(r)
                    # print(self.cost())
                    if r:
                        extra_count += 1
                        # print(f"Package {package_id} loaded in ULD {r}, remaining = {num_unloaded - extra_count}")
                        break
                # print(package)   
                
                
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