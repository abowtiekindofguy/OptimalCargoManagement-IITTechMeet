from package import Package
from uld import ULD

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
        weight_capacity=uld_data[4]
        ulds[uld_id] = ULD(str(uld_id), int(length), int(width), int(height), int(weight_capacity))
        line_index += 1

    package_count = int(lines[line_index]) 
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

    K = int(lines[line_index]) 

    return ulds, packages, K

def parse_output(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    total_cost, total_packages, priority_ULDs = map(int, lines[0].strip().split(','))
    packages = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        package_id = parts[0]
        uld_id = parts[1]
        coords = tuple(map(int, parts[2:]))
        packages.append((package_id, uld_id, coords))
    return total_cost, total_packages, priority_ULDs, packages