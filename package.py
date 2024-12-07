import random

class Package:
    """
    Represents a package with physical dimensions, weight, priority, and loading details.

    Attributes:
        package_id (str): Unique identifier for the package.
        length (int): Length of the package.
        width (int): Width of the package.
        height (int): Height of the package.
        weight (int): Weight of the package.
        priority (int): Priority level (1 for priority, 0 otherwise).
        delay (int): Acceptable delay in loading the package.
        corners (list[tuple[int, int, int]]): Coordinates of the package's corners.
        loaded (str or None): ID of the ULD where the package is loaded, or `None` if not loaded.
    """
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
        """
        Calculates the geometric center of the package based on its corners.

        Returns:
            tuple[float, float, float]: The (x, y, z) coordinates of the package's center.
        """
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
        """
        Returns a string representation of the package, including its ID, priority, loading status, reference corner, and delay.

        Returns:
            str: String representation of the package.
        """
        if self.loaded is not None:
            return f"Package(Pkg ID: {self.package_id}, Priority: {self.priority}, Loaded: {self.loaded}, Reference Corner: {self.corners[0]}, Delay: {self.delay})"
        else:
            return f"Package(Pkg ID: {self.package_id}, Priority: {self.priority}, Loaded: {self.loaded}, Reference Corner: {self.corners}, Delay: {self.delay})"

    def generate_corners(self, reference_corner):
        """
        Generates the eight corners of the package based on its reference corner.

        Args:
            reference_corner (tuple[int, int, int]): The (x, y, z) coordinates of the reference corner.

        Returns:
            list[tuple[int, int, int]]: List of coordinates representing the package's corners.
        """
        x, y, z = reference_corner
        self.corners = [
            (x, y, z), 
            (x + self.length, y, z), 
            (x, y + self.width, z), 
            (x + self.length, y + self.width, z), 
            (x, y, z + self.height), 
            (x + self.length, y, z + self.height), 
            (x, y + self.width, z + self.height), 
            (x + self.length, y + self.width, z + self.height)
        ]
        return self.corners

    def reorient(self, z_index):
        """
        Reorients the package dimensions based on the specified z-index.

        Args:
            z_index (int): The index indicating the new orientation axis (1-based).

        Modifies:
            Updates the package's dimensions to reflect the new orientation.
        """
        dimension_list = [self.length, self.width, self.height]
        self.width = dimension_list[z_index - 1]
        rest_dimensions = [dimension_list[i] for i in range(3) if i != z_index - 1]
        self.height = max(rest_dimensions)
        self.length = min(rest_dimensions)

def single_dimension_match(package_1_dimensions, package_2_dimensions):
    """
    Checks if any dimension of one package matches any dimension of another package.

    Args:
        package_1_dimensions (list[int]): Dimensions of the first package.
        package_2_dimensions (list[int]): Dimensions of the second package.

    Returns:
        bool: True if there is a matching dimension, False otherwise.
    """
    for i in range(len(package_1_dimensions)):
        if package_1_dimensions[i] in package_2_dimensions:
            return True
    return False

def single_dimension_match_by_index(package_1_dimensions, package_2_dimensions, index):
    """
    Checks if a specific dimension of one package matches any dimension of another package.

    Args:
        package_1_dimensions (list[int]): Dimensions of the first package.
        package_2_dimensions (list[int]): Dimensions of the second package.
        index (int): Index of the dimension to check (0-based).

    Returns:
        int or bool: The index (1-based) of the matching dimension in `package_2_dimensions`, or False if no match.
    """
    if package_1_dimensions[index] in package_2_dimensions:
        return package_2_dimensions.index(package_1_dimensions[index]) + 1
    return False

def crainic_sorting(packages_list, group_on_dimensions=False, reverse=False):
    """
    Sorts packages using Crainic's grouping and matching heuristic based on dimensions.

    Args:
        packages_list (list[Package]): List of packages to be sorted.
        group_on_dimensions (bool, optional): Whether to group packages by a specific dimension. Defaults to False.
        reverse (bool, optional): Whether to reverse the sorting order. Defaults to False.

    Returns:
        list[tuple[str, int]]: List of package IDs with their corresponding orientations, in sorted order.
    """
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
                    if package_id != other_package_id and single_dimension_match_by_index(package_dimensions, other_package_dimensions, i - 1) and other_package_id not in matched_packages:
                        dim_matches_map[i].append((other_package_id, single_dimension_match_by_index(package_dimensions, other_package_dimensions, i - 1)))

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
        dimension_to_group = main_package_dimensions[first_package_orientation - 1]

        groups.append(new_group)
        dimension_group_order[dimension_to_group] = new_group

    if group_on_dimensions:
        sorted_groups = sorted(dimension_group_order.keys(), reverse=reverse)
        for group_key in sorted_groups:
            order += dimension_group_order[group_key]
    else:
        random.shuffle(groups)
        for group in groups:
            order += group
    return order
