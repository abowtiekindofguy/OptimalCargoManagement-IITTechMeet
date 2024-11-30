import random

class Package:
    def __init__(self, package_id, length, width, height, weight, priority, delay):
        self.package_id = package_id
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.priority = 1 if priority == "Priority" else 0
        self.delay = int(delay)
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
        return f"Package({self.package_id}, {self.priority}, {self.loaded}, {self.corners})"    

    def generate_corners(self, reference_corner):
        x, y, z = reference_corner
        self.corners = [(x, y, z), (x + self.length, y, z), (x, y + self.width, z), (x + self.length, y + self.width, z), (x, y, z + self.height), (x + self.length, y, z + self.height), (x, y + self.width, z + self.height), (x + self.length, y + self.width, z + self.height)]
        return self.corners
    
    def reorient(self, z_index):
        dimension_list = [self.length, self.width, self.height]
        self.height = dimension_list[z_index-1]
        rest_dimensions = [dimension_list[i] for i in range(3) if i != z_index-1]
        self.length = max(rest_dimensions)
        self.width = min(rest_dimensions)
        
    
    
def single_dimension_match(package_1_dimensions, package_2_dimensions):
    for i in range(3):
        if package_1_dimensions[i] in package_2_dimensions:
            return True
    return False

def single_dimension_match_by_index(package_1_dimensions, package_2_dimensions, index):
    if package_1_dimensions[index] in package_2_dimensions:
        return (package_2_dimensions.index(package_1_dimensions[index])+1)
    return False
    
def crainic_sorting(packages_dictionary, group_on_dim = False, opposite_order = False):
    packages_dimensions_dict = {}
    for package_id, package in packages_dictionary.items():
        packages_dimensions_dict[package_id] = [package.length, package.width, package.height]
    match_by_one_dimension = {}
    matched_packages = set()
    for package_id, package_dimensions in packages_dimensions_dict.items():
        if package_id not in matched_packages:
            matches = {1: [], 2: [], 3: []}
            for i in range(3):
                for other_package_id, other_package_dimensions in packages_dimensions_dict.items():
                    if package_id != other_package_id and single_dimension_match_by_index(package_dimensions, other_package_dimensions, i) and other_package_id not in matched_packages:
                        matches[i+1].append((other_package_id, single_dimension_match_by_index(package_dimensions, other_package_dimensions, i)))   
            max_match_index = max(matches, key=lambda x: len(matches[x]))
            match_by_one_dimension[package_id] = (matches[max_match_index], max_match_index)
            for match in matches[max_match_index]:
                matched_packages.add(match[0])
            matched_packages.add(package_id)

    order = []
    groups = []
    dimension_group_order = {}
    for package_id, item_details in match_by_one_dimension.items():
        to_append = []
        to_append.append((package_id, item_details[1]))
        for packages in item_details[0]:
            to_append.append(packages)
        random.shuffle(to_append)
        groups.append(to_append)
        main_package = packages_dimensions_dict[package_id]
        dimension_to_group_idx = item_details[1]
        dimension_to_group = main_package[dimension_to_group_idx-1]
        dimension_group_order[dimension_to_group] = to_append
    if group_on_dim:
        if opposite_order:
            sorted_groups = sorted(dimension_group_order.keys(), reverse = True)
        else:
            sorted_groups = sorted(dimension_group_order.keys())
        for group in sorted_groups:
            order += dimension_group_order[group]
    else:   
        random.shuffle(groups)  
        for group in groups:
            order += group
    return order
    
    

            
    