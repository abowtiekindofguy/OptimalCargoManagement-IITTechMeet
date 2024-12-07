import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from random import shuffle
from package import Package
from uld import ULD
from io_utils import parse_input, parse_output

def print_summary(ulds, packages):
    print("ULDs:")
    for uld in ulds.values():
        print(uld)

    print("\nPackages:")
    for pkg in packages.values():
        print(pkg)


def visualize_packing(total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show=False):
    # Group packages by ULD ID
    priority_packages_count = 0
    economy_packages_count = 0
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

        eco_cost_uld = 0
        pri_cost_uld = 0
        filled_capacity_uld = 0
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
            # color = packages1[package_id].priority == "Priority" and priority_color or economy_color
    
            filled_capacity_uld += packages1[package_id].weight
            if packages1[package_id].priority == 1:
                priority_packages_count += 1
                pri_cost_uld += 1
                color = priority_color
            else:
                economy_packages_count += 1
                eco_cost_uld += 1   
                color = economy_color
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
        ax.set_title(f"ULD: {uld_id} Visualization\nPriority Packages Packed: {pri_cost_uld}, Economy Packages Packed: {eco_cost_uld}")

        
        plt.savefig(f"output/{output_file}_{uld_id}.png")
            
        # print(uld_id, "Filled Capacity: ", filled_capacity_uld)
        print(uld_id, "Max Allowed Capacity: ", ulds[uld_id].capacity, "Filled Capacity: ", filled_capacity_uld)
        print(uld_id, "Priority Packages:", pri_cost_uld, "Economy Packages:", eco_cost_uld)
        
    print(f"Priority Packages: {priority_packages_count}, Economy Packages: {economy_packages_count}")


def visualize_packing3d(
    total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show=True
):
    # Group packages by ULD ID
    priority_packages_count = 0
    economy_packages_count = 0
    uld_groups = {}
    for package_id, uld_id, coords in packages:
        if uld_id not in uld_groups:
            uld_groups[uld_id] = []
        uld_groups[uld_id].append((package_id, coords))

    priority_color = "green"
    economy_color = "pink"

    # Set up the combined figure
    num_uld = len(uld_groups)
    rows, cols = 2, 3  # Fixed grid size (2 rows and 3 columns)
    fig = plt.figure(figsize=(15, 10))  # Adjust figure size for clarity
    plot_idx = 1

    for uld_id, uld_packages in uld_groups.items():
        if uld_id == "NONE":
            continue

        ax = fig.add_subplot(rows, cols, plot_idx, projection='3d')
        plot_idx += 1

        x_min, y_min, z_min = 0, 0, 0
        x_max, y_max, z_max = ulds[uld_id].length, ulds[uld_id].width, ulds[uld_id].height

        eco_cost_uld = 0
        pri_cost_uld = 0
        filled_capacity_uld = 0

        for package_id, coords in uld_packages:
            x0, y0, z0, x1, y1, z1 = coords

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

            filled_capacity_uld += packages1[package_id].weight
            if packages1[package_id].priority == 1:
                priority_packages_count += 1
                pri_cost_uld += 1
                color = priority_color
            else:
                economy_packages_count += 1
                eco_cost_uld += 1   
                color = economy_color

            ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='black', alpha=0.5))
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, package_id, fontsize=6)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_zlim(z_min, z_max)
        ax.set_title(f"ULD: {uld_id}\nPriority: {pri_cost_uld}, Economy: {eco_cost_uld}")

        # print(uld_id, "Max Allowed Capacity: ", ulds[uld_id].capacity, "Filled Capacity: ", filled_capacity_uld)
        # print(uld_id, "Priority Packages:", pri_cost_uld, "Economy Packages:", eco_cost_uld)

        # Stop if the grid is filled
        if plot_idx > rows * cols:
            print("Only the first 6 ULDs will be displayed due to grid size.")
            break

    plt.tight_layout()
    # if show:
    #     plt.show()
    #     plt.savefig(f"output/{output_file}_combined.png")
    # else:
    #     plt.savefig(f"output/{output_file}_combined.png")
    plt.show()
    # plt.savefig(f"output/{output_file}_combined.png")

    # print(f"Priority Packages: {priority_packages_count}, Economy Packages: {economy_packages_count}")



def visualize(input_file, output_file, show=False):
    ulds, packages1, k = parse_input(input_file)
    t = (list(ulds.values()))
    total_cost, total_packages, priority_ULDs, packages = parse_output(f"output/{output_file}")
    if show:
        visualize_packing(total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show)
        visualize_packing3d(total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show)
    else:
        visualize_packing(total_cost, packages1, ulds, total_packages, priority_ULDs, packages, output_file, show)
    
if __name__ == "__main__":
    visualize(sys.argv[1], sys.argv[2], 1)
    