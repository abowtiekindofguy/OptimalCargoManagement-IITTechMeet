import random
import enum

class ReorientationMethod(enum.Enum):
    pass


class Package:
    def __init__(self, package_id, length, width, height, weight, priority, delay):
        self.package_id = package_id
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.priority = priority
        self.delay = delay
        self.corners = []
        self.loaded = None
        
    def center(self):
        x_center, y_center, z_center = 0, 0, 0
        for corner in self.corners:
            x_center += corner[0]
            y_center += corner[1]
            z_center += corner[2]
        x_center /= 8
        y_center /= 8
        z_center /= 8
        return x_center, y_center, z_center
        
    def __repr__(self):
        if self.loaded is not None:
            return f"Package(Pkg ID: {self.package_id}, Priority: {self.priority}, Loaded: {self.loaded}, Reference Corner: {self.corners[0]}, Delay: {self.delay})"
        else:
            return f"Package(Pkg ID: {self.package_id}, Priority: {self.priority}, Loaded: {self.loaded}, Reference Corner: {self.corners}, Delay: {self.delay})"    

    def generate_corners(self, reference_corner):
        x, y, z = reference_corner
        self.corners = [(x, y, z), (x + self.length, y, z), (x, y + self.width, z), (x + self.length, y + self.width, z), (x, y, z + self.height), (x + self.length, y, z + self.height), (x, y + self.width, z + self.height), (x + self.length, y + self.width, z + self.height)]
        return self.corners
    
    def reorient(self, z_index):
        dimension_list = [self.length, self.width, self.height]
        # self.height = dimension_list[z_index-1]
        # rest_dimensions = [dimension_list[i] for i in range(3) if i != z_index-1]
        # self.length = max(rest_dimensions)
        # self.width = min(rest_dimensions)
        self.width = dimension_list[z_index-1]
        rest_dimensions = [dimension_list[i] for i in range(3) if i != z_index-1]
        # self.height = min(rest_dimensions)
        # self.length = max(rest_dimensions)
        self.height = max(rest_dimensions)
        self.length = min(rest_dimensions)
        
    
    
def single_dimension_match(package_1_dimensions, package_2_dimensions):
    for i in range(len(package_1_dimensions)):
        if package_1_dimensions[i] in package_2_dimensions:
            return True
    return False

def single_dimension_match_by_index(package_1_dimensions, package_2_dimensions, index):
    if package_1_dimensions[index] in package_2_dimensions:
        return (package_2_dimensions.index(package_1_dimensions[index])+1)
    return False
    
def crainic_sorting(packages_list, group_on_dimensions = False, reverse = False):
    packages_dimensions_dict = {}
    for package in packages_list:
        packages_dimensions_dict[package.package_id] = [package.length, package.width, package.height]
        
    matches_by_dimension = {}
    matched_packages = set()
    for package_id, package_dimensions in packages_dimensions_dict.items():
        if package_id not in matched_packages:
            dim_matches_map = {1: [], 2: [], 3: []}
            for i in dim_matches_map.keys():
                for other_package_id, other_package_dimensions in packages_dimensions_dict.items():
                    if package_id != other_package_id and single_dimension_match_by_index(package_dimensions, other_package_dimensions, i-1) and other_package_id not in matched_packages:
                        dim_matches_map[i].append((other_package_id, single_dimension_match_by_index(package_dimensions, other_package_dimensions, i-1)))   
                        
            max_match_index = max(dim_matches_map, key=lambda x: len(dim_matches_map[x]))
            matches_by_dimension[package_id] = (dim_matches_map[max_match_index], max_match_index)
            for match in dim_matches_map[max_match_index]:
                matched_packages.add(match[0])
            matched_packages.add(package_id)

    order = []
    groups = []
    dimension_group_order = {}
    
    for package_id, item_details in matches_by_dimension.items():
        first_package, first_package_orientation = package_id, item_details[1]
        new_group = [(first_package, first_package_orientation)]
        for package_orientation_pair in item_details[0]:
            new_group.append(package_orientation_pair)
        random.shuffle(new_group)
        main_package_dimensions = packages_dimensions_dict[first_package]
        # dimension_to_group_idx = item_details[1]
        dimension_to_group = main_package_dimensions[first_package_orientation-1]
        # #all dimensions of the main package
        # main_pkg = packages_dictionary[package_id]
        # all_dimension_of_main_package = [main_pkg.length, main_pkg.width, main_pkg.height]
        # all_dimension_of_main_package.remove(dimension_to_group)
        # def max_dimension_apart_from_grouped(package_id, dim_to_remove):
        #     package = packages_dictionary[package_id]
        #     package_dimensions = [package.length, package.width, package.height]
        #     package_dimensions.remove(dim_to_remove)
        #     return max(package_dimensions)
        
        # to_append = sorted(to_append, key = lambda x: max_dimension_apart_from_grouped(x[0], dimension_to_group), reverse = True)
            
        groups.append(new_group)
        dimension_group_order[dimension_to_group] = new_group
        
    if group_on_dimensions:
        sorted_groups = sorted(dimension_group_order.keys(), reverse = reverse)
        for group_key in sorted_groups: order += dimension_group_order[group_key]
    else:   
        random.shuffle(groups)  
        for group in groups: order += group
    return order