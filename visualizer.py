import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from io_utils import parse_input, parse_output


def add_package_to_plot(ax, coords, package_id, color):
    """Add a package to the 3D plot."""
    x0, y0, z0, x1, y1, z1 = coords
    vertices = [
        [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1],
    ]
    faces = [
        [vertices[i] for i in face] for face in [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]
        ]
    ]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='black', alpha=0.5))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, package_id, fontsize=6)


def plot_uld(ax, uld_id, uld_packages, uld_dims, packages1, priority_color, economy_color):
    """Plot a single ULD's packages."""
    x_max, y_max, z_max = uld_dims
    pri_cost, eco_cost, filled_capacity = 0, 0, 0

    for package_id, coords in uld_packages:
        color = priority_color if packages1[package_id].priority == 1 else economy_color
        pri_cost += packages1[package_id].priority == 1
        eco_cost += packages1[package_id].priority != 1
        filled_capacity += packages1[package_id].weight
        add_package_to_plot(ax, coords, package_id, color)

    ax.set(xlabel="X", ylabel="Y", zlabel="Z", xlim=(0, x_max), ylim=(0, y_max), zlim=(0, z_max))
    ax.set_title(f"ULD: {uld_id}\nPriority: {pri_cost}, Economy: {eco_cost}")
    return pri_cost, eco_cost, filled_capacity


def visualize_packing(packages, packages1, ulds, output_file, rows=2, cols=3, combined=False):
    """Visualize the ULD packing either individually or in a combined grid."""
    uld_groups = {uld_id: [] for uld_id in ulds}
    for package_id, uld_id, coords in packages:
        if uld_id in uld_groups:
            uld_groups[uld_id].append((package_id, coords))

    priority_color, economy_color = "green", "pink"
    total_priority, total_economy = 0, 0

    fig = plt.figure(figsize=(15, 10)) if combined else None
    plot_idx = 1

    for uld_id, uld_packages in uld_groups.items():
        if not uld_packages or uld_id == "NONE":
            continue

        ax = fig.add_subplot(rows, cols, plot_idx, projection='3d') if combined else plt.figure().add_subplot(111, projection='3d')
        plot_idx += 1

        uld_dims = (ulds[uld_id].length, ulds[uld_id].width, ulds[uld_id].height)
        pri_cost, eco_cost, filled_capacity = plot_uld(ax, uld_id, uld_packages, uld_dims, packages1, priority_color, economy_color)

        total_priority += pri_cost
        total_economy += eco_cost
        print(f"{uld_id} Max Capacity: {ulds[uld_id].capacity}, Filled: {filled_capacity}")
        if not combined:
            plt.savefig(f"{output_file}_{uld_id}.png")
            plt.close()

        if combined and plot_idx > rows * cols:
            print("Grid filled. Remaining ULDs will not be displayed.")
            break

    if combined:
        plt.tight_layout()
        plt.savefig(f"{output_file}_combined.png")
        plt.show()

    print(f"Total Priority Packages: {total_priority}, Economy Packages: {total_economy}")


def visualize(input_file, output_file, show=False):
    ulds, packages1, _ = parse_input(input_file)
    total_cost, total_packages, priority_ULDs, packages = parse_output(output_file)

    combined = show  # Show all ULDs in a single plot if `show` is True
    visualize_packing(packages, packages1, ulds, output_file, combined=combined)


if __name__ == "__main__":
    visualize(sys.argv[1], sys.argv[2], show=True)
