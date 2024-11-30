import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from random import shuffle

class ULD:
    def __init__(self, uld_id, length, width, height, capacity):
        self.uld_id = uld_id
        self.length = length
        self.width = width
        self.height = height
        self.capacity = capacity 
        self.used_volume = 0
        self.used_weight = 0
        self.packages=[]

    def __repr__(self):
        return f"ULD({self.uld_id}, {self.length}, {self.width}, {self.height}, {self.capacity})"


class Package:
    def __init__(self, package_id, length, width, height, weight, priority, delay):
        self.package_id = package_id
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.priority = priority
        self.delay = delay

    def __repr__(self):
        return f"Package({self.package_id}, {self.length}, {self.width}, {self.height}, {self.weight}, {self.priority}, {self.delay})"


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

# TODO : First/Best Fit Implementation is left
# def pack_ulds(ulds, packages, k, out): 
#     packages.sort(key=lambda p: (p.priority, -p.length * p.width * p.height))

#     for package in packages:
#         placed = False
#         for uld in ulds:
#             if uld.used_volume + package.length * package.width * package.height <= uld.capacity and uld.used_weight + package.weight <= k:
#                 uld.packages.append((package.package_id, uld.uld_id, len(uld.packages), 0, 0, 0, package.length, package.width, package.height))
#                 uld.used_volume += package.length * package.width * package.height
#                 uld.used_weight += package.weight
#                 placed = True
#                 break
#         if not placed:
#             ulds.append(ULD(f"ULD{len(ulds) + 1}", package.length, package.width, package.height, k))
#             ulds[-1].packages.append((package.package_id, ulds[-1].uld_id, 0, 0, 0, package.length, package.width, package.height))
#             ulds[-1].used_volume = package.length * package.width * package.height
#             ulds[-1].used_weight = package.weight

#     total_volume = sum(uld.used_volume for uld in ulds)
#     total_weight = sum(uld.used_weight for uld in ulds)
#     num_ulds = len(ulds)

#     output = []
#     for uld in ulds:
#         for package_id, uld_id, x, y, z, length, width, height in uld.packages:
#             output.append((package_id, uld_id, x, y, z, length, width, height))
#     with open(out, 'w') as file:
#         file.write(f"{total_volume},{total_weight},{num_ulds}")
#         file.write("\n")
#         for line in output:
#             file.write(",".join(map(str, line)))
#             file.write("\n")
#     return 

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


def print_summary(ulds, packages):
    print("ULDs:")
    for uld in ulds.values():
        print(uld)

    print("\nPackages:")
    for pkg in packages.values():
        print(pkg)


def visualize_packing(total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show=False):
    # Group packages by ULD ID
    uld_groups = {}
    for package_id, uld_id, coords in packages:
        if uld_id not in uld_groups:
            uld_groups[uld_id] = []
        uld_groups[uld_id].append((package_id, coords))

    priority_color = "green"
    economy_color = "pink"
    for uld_id, uld_packages in uld_groups.items():
        if uld_id == "NONE":
            continue
        
        number_of_packages = len(uld_packages)

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')

        x_min, y_min, z_min = float('inf'), float('inf'), float('inf')
        x_max, y_max, z_max = float('-inf'), float('-inf'), float('-inf')

        for package_id, coords in uld_packages:
            x0, y0, z0, x1, y1, z1 = coords

            x_min, y_min, z_min = 0, 0, 0
            x_max, y_max, z_max = ulds[uld_id].length, ulds[uld_id].width, ulds[uld_id].height

            vertices = [
                [x0, y0, z0],
                [x1, y0, z0],
                [x1, y1, z0],
                [x0, y1, z0],
                [x0, y0, z1],
                [x1, y0, z1],
                [x1, y1, z1],
                [x0, y1, z1],
            ]

            faces = [
                [vertices[i] for i in [0, 1, 2, 3]],  
                [vertices[i] for i in [4, 5, 6, 7]], 
                [vertices[i] for i in [0, 1, 5, 4]],
                [vertices[i] for i in [2, 3, 7, 6]], 
                [vertices[i] for i in [1, 2, 6, 5]],
                [vertices[i] for i in [0, 3, 7, 4]],  
            ]
            color = packages1[package_id].priority == "Priority" and priority_color or economy_color
            # for face in faces:
            #     ax.plot([v[0] for v in face] + [face[0][0]], 
            #             [v[1] for v in face] + [face[0][1]], 
            #             [v[2] for v in face] + [face[0][2]], color=color)
            ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='black', alpha=0.1))

            ax.text((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, package_id, fontsize=8)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_zlim(z_min, z_max)
        ax.set_title(f"ULD: {uld_id} Visualization\nTotal Cost: {total_cost}, Total Packages: {total_packages}, Priority ULDs: {number_of_packages}")

        if show:
            plt.show()
        else:
            plt.savefig(f"output/{output_file}_{uld_id}.png")


def visualize(input_file, output_file, show=False):
    ulds, packages1, k = parse_input(input_file)
    t = (list(ulds.values()))
    total_cost, total_packages, priority_ULDs, packages = parse_output(f"output/{output_file}")
    visualize_packing(total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show)
    
if __name__ == "__main__":
    visualize(sys.argv[1], sys.argv[2], True)
    