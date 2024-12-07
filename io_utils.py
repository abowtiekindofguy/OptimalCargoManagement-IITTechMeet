from package import Package
from uld import ULD

def parse_input(file):
    """
    Parses the input file to extract ULD and package data along with the optimization parameter K.

    Args:
        file (str): Path to the input file.

    Returns:
        tuple: A tuple containing:
            - ulds (dict): A dictionary mapping ULD IDs to ULD objects.
            - packages (dict): A dictionary mapping package IDs to Package objects.
            - K (int): Optimization parameter indicating the number of iterations or priority level.
    """
    with open(file, 'r') as file:
        lines = file.readlines()
    
    uld_count = int(lines[0])  # Number of ULDs
    ulds = {}
    line_index = 1
    for _ in range(uld_count):
        uld_data = lines[line_index].split(",")
        uld_id = uld_data[0]
        length = uld_data[1]
        width = uld_data[2]
        height = uld_data[3]
        weight_capacity = uld_data[4]
        ulds[uld_id] = ULD(str(uld_id), int(length), int(width), int(height), int(weight_capacity))
        line_index += 1

    package_count = int(lines[line_index])  # Number of packages
    packages = {}
    line_index += 1
    for _ in range(package_count):
        package_data = lines[line_index].split(",")
        package_id, length, width, height, weight, priority, delay = package_data
        priority_string = priority.strip()
        priority = 1 if priority_string == 'Priority' else 0
        weight = int(weight)
        delay = int(delay)
        packages[package_id] = Package(str(package_id), int(length), int(width), int(height), weight, priority, delay)
        line_index += 1

    K = int(lines[line_index])  # Optimization parameter

    return ulds, packages, K

def parse_output(file_path):
    """
    Parses the output file to extract information about the optimization results.

    Args:
        file_path (str): Path to the output file.

    Returns:
        tuple: A tuple containing:
            - total_cost (int): The total cost incurred in the packing solution.
            - total_packages (int): The total number of packages successfully packed.
            - priority_ULDs (int): The number of ULDs used for priority packages.
            - packages (list): A list of tuples, each representing a packed package in the form:
              (package_id (str), uld_id (str), coords (tuple[int, int, int])).
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Parse summary line
    total_cost, total_packages, priority_ULDs = map(int, lines[0].strip().split(','))
    packages = []

    # Parse package details
    for line in lines[1:]:
        parts = line.strip().split(',')
        package_id = parts[0]
        uld_id = parts[1]
        coords = tuple(map(int, parts[2:]))
        packages.append((package_id, uld_id, coords))
    
    return total_cost, total_packages, priority_ULDs, packages
