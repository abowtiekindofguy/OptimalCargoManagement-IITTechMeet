import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from collections import namedtuple
import itertools


def plot_3d_objects(objects):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for idx, obj in enumerate(objects):
        x, y, z = obj.origin.tolist()
        l = obj.length
        w = obj.width
        h = obj.height

        vertices = [
            [x, y, z],  # bottom vertices
            [x + l, y, z],
            [x + l, y + h, z],
            [x, y + h, z],
            [x, y, z + w],  # top vertices
            [x + l, y, z + w],
            [x + l, y + h, z + w],
            [x, y + h, z + w]
        ]
        
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
            [vertices[3], vertices[0], vertices[4], vertices[7]],  # left
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
            [vertices[4], vertices[5], vertices[6], vertices[7]]   # top
        ]

        if idx!=0:
            ax.add_collection3d(Poly3DCollection(faces, alpha=0.5, edgecolor='k'))
            
        if idx==0:
            ax.add_collection3d(Poly3DCollection(faces, alpha=0.1, edgecolor='k', facecolors='red'))
    
    # Set labels and aspect
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    
    plt.show()
    
def plot(packing_solution):
    for container in packing_solution:
        if len(container) > 1:
            plot_3d_objects(container)
        else:
            print("Empty container")


class PackageMatcher:
    def __init__(self, packing_solution, uld_ids, package_ids):
        # print(packing_solution)
        
        self.packing_solution = packing_solution
        self.package_association = {}
        
        # Create reverse mappings for ULDs and packages
        # reverse_uld_ids = {v: [k] if v not in uld_ids.values() else reverse_uld_ids[v] + [k] for k, v in uld_ids.items()}
        reverse_uld_ids = {}
        for k, dims in uld_ids.items():
            reverse_uld_ids.setdefault(dims, []).append(k)
        reverse_package_ids = {}
        for k, dims in package_ids.items():
            for perm in set(itertools.permutations(dims)):  # All unique permutations
                reverse_package_ids.setdefault(perm, []).append((k, perm))
        
        marked_ulds, marked_packages = set(), set()

        # Match ULDs and packages
        for container in packing_solution:
            if len(container) > 1:
                container_dims = (container[0].length, container[0].width, container[0].height)
                uld_id = next((uid for uid in reverse_uld_ids.get(container_dims, []) if uid not in marked_ulds), None)
                # print(uld_id)
                if uld_id is None:
                    raise Exception(f"No ULD found for container dimensions: {container_dims}")
                marked_ulds.add(uld_id)

                for package in container[1:]:
                    package_dims = (package.length, package.width, package.height)
                    possible_ids = [
                        pkg for dims in itertools.permutations(package_dims) 
                        for pkg in reverse_package_ids.get(dims, [])
                    ]
                    package_data = next((pkg for pkg in possible_ids if pkg[0] not in marked_packages), None)
                    # print(package_data)
                    if package_data is None:
                        raise Exception(f"No package found for dimensions: {package_dims}")
                    
                    package_id, orientation = package_data
                    marked_packages.add(package_data)
                    self.package_association[package_id] = (
                        uld_id,
                        (package.origin.tolist()[0], package.origin.tolist()[2], package.origin.tolist()[1]),
                        orientation
                    )

    def get_parent_uld(self, package_id):
        return self.package_association.get(package_id, (None,))[0]
    
    def get_package_position(self, package_id):
        return self.package_association.get(package_id, (None, None))[1]
    
    def get_package_orientation(self, package_id):
        return self.package_association.get(package_id, (None, None, None))[2]
    
    def is_placed(self, package_id):
        return package_id in self.package_association