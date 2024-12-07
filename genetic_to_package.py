import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from collections import namedtuple
import itertools


def plot_3d_objects(objects):
    """
    Plots 3D objects using the given list of objects with specified dimensions and origin.

    Args:
        objects (list): A list of objects with attributes `origin`, `length`, `width`, and `height`.
    
    Returns:
        None: Displays a 3D plot of the objects.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for idx, obj in enumerate(objects):
        x, y, z = obj.origin.tolist()
        l = obj.length
        w = obj.width
        h = obj.height

        vertices = [
            [x, y, z],  
            [x + l, y, z],
            [x + l, y + h, z],
            [x, y + h, z],
            [x, y, z + w],
            [x + l, y, z + w],
            [x + l, y + h, z + w],
            [x, y + h, z + w]
        ]
        
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  
            [vertices[1], vertices[2], vertices[6], vertices[5]],  
            [vertices[2], vertices[3], vertices[7], vertices[6]], 
            [vertices[3], vertices[0], vertices[4], vertices[7]],
            [vertices[0], vertices[1], vertices[2], vertices[3]],  
            [vertices[4], vertices[5], vertices[6], vertices[7]]   
        ]

        if idx != 0:
            ax.add_collection3d(Poly3DCollection(faces, alpha=0.5, edgecolor='k'))
            
        if idx == 0:
            ax.add_collection3d(Poly3DCollection(faces, alpha=0.1, edgecolor='k', facecolors='red'))
    
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")
    ax.set_box_aspect([1, 1, 1])
    
    plt.show()


def plot(packing_solution):
    """
    Plots the 3D objects in the packing solution. Displays objects only if the container has more than one object.

    Args:
        packing_solution (list): A list of containers, where each container is a list of objects.

    Returns:
        None: Displays the 3D plot of objects in containers.
    """
    for container in packing_solution:
        if len(container) > 1:
            plot_3d_objects(container)
        else:
            print("Empty container")


class PackageMatcher:
    """
    Matches packages to ULDs based on their dimensions and packing solution, storing the associations.

    Args:
        packing_solution (list): A list of containers, where each container is a list of objects (packages).
        uld_ids (dict): A dictionary where the keys are ULD IDs and values are the ULD dimensions.
        package_ids (dict): A dictionary where the keys are package IDs and values are the package dimensions.
    
    Returns:
        None: Initializes the package matching by associating packages with ULDs.
    """
    def __init__(self, packing_solution, uld_ids, package_ids):        
        self.packing_solution = packing_solution
        self.package_association = {}
        
        reverse_uld_ids = {}
        for k, dims in uld_ids.items():
            reverse_uld_ids.setdefault(dims, []).append(k)
        reverse_package_ids = {}
        for k, dims in package_ids.items():
            for perm in set(itertools.permutations(dims)):
                reverse_package_ids.setdefault(perm, []).append((k, perm))
        
        marked_ulds, marked_packages = set(), set()

        for container in packing_solution:
            if len(container) > 1:
                container_dims = (container[0].length, container[0].width, container[0].height)
                uld_id = next((uid for uid in reverse_uld_ids.get(container_dims, []) if uid not in marked_ulds), None)
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
        """
        Retrieves the ULD ID associated with a given package ID.

        @params:
            package_id (str): The package ID.

        @return:
            str: The ULD ID associated with the package, or None if no association exists.
        """
        return self.package_association.get(package_id, (None,))[0]
    
    def get_package_position(self, package_id):
        """
        Retrieves the position of the package in the 3D space.

        @params:
            package_id (str): The package ID.

        @return:
            tuple: A tuple containing the position (x, y, z) of the package, or None if not placed.
        """
        return self.package_association.get(package_id, (None, None))[1]
    
    def get_package_orientation(self, package_id):
        """
        Retrieves the orientation of the package.

        @params:
            package_id (str): The package ID.

        @return:
            tuple: A tuple representing the orientation of the package, or None if not placed.
        """
        return self.package_association.get(package_id, (None, None, None))[2]
    
    def is_placed(self, package_id):
        """
        Checks if a given package has been placed in a ULD.

        @params:
            package_id (str): The package ID.

        @return:
            bool: True if the package is placed, otherwise False.
        """
        return package_id in self.package_association
