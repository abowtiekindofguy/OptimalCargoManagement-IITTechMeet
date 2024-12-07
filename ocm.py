import random   
from package import crainic_sorting
from genetic import GeneticAlgorithm

class OptimalCargoManagement(object):
    def __init__(self, ulds, packages, K, verbose = False):
        self.ulds = ulds
        self.packages = packages
        self.K = K
        self.package_ordering = None
        self.non_priority_ordering = None
        self.priority_ordering = None
        self.verbose = verbose
        
    def log(self, message):
        if self.verbose: print(message)
        
    def add_uld(self, uld):
        self.ulds[uld.uld_id] = uld 
        
    def add_package(self, package):
        self.packages[package.package_id] = package
        
    def cost(self, only_priority = False):
        total_cost = 0
        priority_activated_ulds = set()
        for package in self.packages.values():
            if package.loaded is not None and package.priority:
                priority_activated_ulds.add(package.loaded)
        priority_cost = len(priority_activated_ulds)
        
        economy_cost = 0
        for package in self.packages.values():
            if not package.priority and package.loaded is None:
                economy_cost += package.delay
        total_cost = priority_cost * self.K + economy_cost
            
        if only_priority: return priority_cost
        else: return total_cost
        
    def num_packages_loaded(self):
        num_packages_loaded = 0
        for package in self.packages.values():
            if package.loaded is not None:
                num_packages_loaded += 1
                
        return num_packages_loaded
    
    def fit_greedy(self, optional_ordering = None, selected_ulds = None):
        self.log(f"Fitting packages: {len(self.packages)} packages in {len(self.ulds)} ULDs")
        self.log(f"Optional ordering: {True if optional_ordering is not None else False}")   
        if optional_ordering is not None:
            for order in optional_ordering:
                package_id = order[0]
                if selected_ulds is not None:
                    for uld_id in selected_ulds:
                        r = self.ulds[uld_id].uld_fill_greedy(self.packages[package_id])
                        if r: break
                else:
                    for uld_id, uld in self.ulds.items():
                        r = uld.uld_fill_greedy(self.packages[package_id])
                        if r: break
        else:
            for order in self.package_ordering:
                package_id = order[0]
                for uld_id, uld in self.ulds.items():
                    r = uld.uld_fill_greedy(self.packages[package_id])
                    if r: break
        
                    
    def __repr__(self):
        uld_string = "Loaded ULDs:\n"
        for uld in self.ulds.values():
            if uld.filled_coordinates:
                uld_string += f"{uld}\n"
                
        package_string = "Loaded Packages:\n"
        for package in self.packages.values():
            if package.loaded is not None:
                package_string += f"{package}\n"
                
        package_string += "Unloaded Packages:\n"
        for package in self.packages.values():
            if package.loaded is None:
                package_string += f"{package}\n"
        
        ocm_attributes = f"OptimalCargoManagement Attributes = {len(self.ulds)} ULDs, {len(self.packages)} Packages, K = {self.K}"   
        return uld_string + package_string + ocm_attributes
    
    def file_output_ocm(self, filename):
        with open(filename, 'w') as file:
            total_cost = self.cost()
            priority_cost = self.cost(only_priority = True)
            num_packages_loaded = self.num_packages_loaded()
            
            file.write(f"{total_cost},{num_packages_loaded},{priority_cost}\n")
            
            for package in self.packages.values():
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
        self.priority_ordering = priority_ordering
        self.non_priority_ordering = non_priority_ordering
        
        self.log("Package Ordering Created \n")
        
        return priority_ordering, non_priority_ordering
        
    def reorient_packages(self):
        for order in self.package_ordering:
            package_id = order[0]
            order_z_against = order[1]            
            package_to_reorient = self.packages[package_id]
            package_to_reorient.reorient(order_z_against)
            
    def adhoc_additions(self, random_shuffle = False):
        self.log("Performing Ad-Hoc Additions with Random Shuffle: {random_shuffle}")
        
        for uld in self.ulds.values():
            uld.create_cuboid_environment()
        
        unloaded_pkd_ids = []
        for package in self.packages.values():
            if package.loaded is None: unloaded_pkd_ids.append(package.package_id)

        sorted_unloaded_pkd_ids = sorted(unloaded_pkd_ids, key = lambda x: self.packages[x].delay/(max([self.packages[x].height,self.packages[x].width,self.packages[x].length])), reverse = True)
              
        if random_shuffle:
            random.shuffle(sorted_unloaded_pkd_ids)  
                
        adhoc_loaded_packages_count = 0
        
        for package_id in sorted_unloaded_pkd_ids:
            package = self.packages[package_id]
            if package.loaded is None:
                for uld in self.ulds.values():
                    r = uld.fit_in_package(package)
                    if r:
                        adhoc_loaded_packages_count += 1
                        self.log(f"Package {package_id} loaded in ULD {uld.uld_id} via Ad-Hoc Addition")
                        break                
                    
        self.log(f"Ad-Hoc Additions Completed: {adhoc_loaded_packages_count} packages loaded")
                
    def unused_uld_ids(self):
        used_ulds = set()
        for package in self.packages.values():
            used_ulds.add(package.loaded) 
        unused_uld_ids = set(self.ulds.keys()) - used_ulds
        
        return unused_uld_ids
    
    def run_genetic_algorithm(self):
        containers_data = []
        packages_data = []
        for uld in self.ulds.values():
            if uld.uld_id in ['U4', 'U5', 'U6']:
                containers_data.append([uld.length, uld.width, uld.height, uld.uld_id])
            
        for package in self.packages.values():
            if package.priority:
                packages_data.append([package.length, package.width, package.height, package.package_id])
                
        priority_ga_instance = GeneticAlgorithm(uld_dimensions=containers_data, package_dimensions=packages_data)

        priority_ga_solution = priority_ga_instance.run_genetic_algorithm()
        
        for package in self.packages.values():
            if package.priority:
                parent_uld = priority_ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = priority_ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = priority_ga_solution.get_package_orientation(package_id=package.package_id)
                
                package.loaded = parent_uld
                package.length, package.width, package.height = pkg_orientation[0], pkg_orientation[1], pkg_orientation[2]
                package.generate_corners(ref_corner)
                
        unused_uld_ids = self.unused_uld_ids()
        
        for uld_id, uld in self.ulds.items():
            if uld_id in unused_uld_ids:
                uld.refresh()
        
    
        non_priority_delay_dict = {}
        non_priority_volume_dict = {}
    
        
        for package in self.packages.values():
            if not package.priority:
                non_priority_delay_dict[package.package_id] = package.delay
                non_priority_volume_dict[package.package_id] = package.length * package.width * package.height
                
        economy_pkg_ordering = self.non_priority_ordering
        economy_pkg_ordering.sort(key=lambda x: (non_priority_delay_dict[x[0]]) ** 1 / (non_priority_volume_dict[x[0]]) ** 1.2, reverse=True)
        economy_pkg_ordering = economy_pkg_ordering[:150]
        economy_pkg_ordering = [x[0] for x in economy_pkg_ordering]
        
        random.shuffle(economy_pkg_ordering)
        
        eco_containers_data = []
        eco_packages_data = []
        
        for uld_id, uld in self.ulds.items():
            if uld_id in unused_uld_ids:
                eco_containers_data.append([uld.length, uld.width, uld.height, uld_id])
            
        for package_id, package in self.packages.items():
            if not package.priority and package.package_id in economy_pkg_ordering:
                eco_packages_data.append([package.length, package.width, package.height, package.package_id])
        
        
        economy_ga_instance = GeneticAlgorithm(uld_dimensions=eco_containers_data, package_dimensions=eco_packages_data)
        eco_ga_solution = economy_ga_instance.run_genetic_algorithm()   
        
        for package in self.packages.values():
            if not package.priority and package.package_id in economy_pkg_ordering:
                if not eco_ga_solution.is_placed(package_id=package.package_id):
                    continue
                parent_uld = eco_ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = eco_ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = eco_ga_solution.get_package_orientation(package_id=package.package_id)
                
                package.loaded = parent_uld
                package.length, package.width, package.height = pkg_orientation[0], pkg_orientation[1], pkg_orientation[2]
                package.generate_corners(ref_corner)
        
        for package in self.packages.values():
            if package.loaded:
                self.ulds[package.loaded].add_package(package)
                
        