from package import Package
from cuboid import *

class ULD:
    """
    Represents a Unit Load Device (ULD) used for cargo transportation.

    Attributes:
        uld_id (str): Identifier for the ULD.
        length (float): Length of the ULD in units.
        width (float): Width of the ULD in units.
        height (float): Height of the ULD in units.
        capacity (float): Maximum weight capacity of the ULD.
        used_volume (float): Volume currently occupied in the ULD.
        used_weight (float): Weight currently occupied in the ULD.
        packages (dict): Dictionary of packages loaded into the ULD, keyed by package ID.
        x_filled (float): Current filled length in the ULD along the x-dimension.
        y_filled (float): Current filled width in the ULD along the y-dimension.
        z_filled (float): Current filled height in the ULD along the z-dimension.
        last_plane_y (float): Y-coordinate of the last plane filled.
        last_filled_row_z (float): Z-coordinate of the last filled row.
        existing_cuboids (list): List of Cuboid objects representing the occupied space in the ULD.
    """

    def __init__(self, uld_id, length, width, height, capacity):
        """
        Initializes a new ULD object with the given dimensions and capacity.

        Args:
            uld_id (str): Unique identifier for the ULD.
            length (float): Length of the ULD.
            width (float): Width of the ULD.
            height (float): Height of the ULD.
            capacity (float): Maximum weight capacity of the ULD.
        """
        self.uld_id = uld_id
        self.length = length
        self.width = width
        self.height = height
        self.capacity = capacity
        self.used_volume = 0
        self.used_weight = 0
        self.packages = {}
        self.x_filled, self.y_filled, self.z_filled = 0, 0, 0
        self.last_plane_y = 0
        self.last_filled_row_z = 0
        self.existing_cuboids = []

    def cost(self, K):
        """
        Calculates the cost of loading high-priority packages.

        Args:
            K (float): Penalty cost for high-priority packages.

        Returns:
            float: Cost incurred if high-priority packages are present, otherwise 0.
        """
        for package in self.packages.values():
            if package.priority:
                return K
        return 0

    def refresh(self):
        """
        Resets the ULD's state, clearing all loaded packages and occupied dimensions.
        """
        self.used_volume = 0
        self.used_weight = 0
        for package in self.packages.values():
            package.loaded = None
        self.packages = {}
        self.x_filled, self.y_filled, self.z_filled = 0, 0, 0
        self.last_plane_y = 0
        self.last_filled_row_z = 0
        self.existing_cuboids = []

    def add_package(self, package):
        """
        Adds a package to the ULD's package dictionary.

        Args:
            package (Package): The package to be added.
        """
        self.packages[package.package_id] = package

    def __repr__(self):
        """
        Returns a string representation of the ULD object.

        Returns:
            str: String representation of the ULD.
        """
        return f"ULD({self.uld_id}, {self.length}, {self.width}, {self.height}, {self.capacity})"

    def uld_fill_greedy(self, package):
        """
        Attempts to place a package in the ULD using a greedy algorithm.

        Args:
            package (Package): The package to be placed.

        Returns:
            bool: True if the package was successfully placed, otherwise False.
        """
        # Try to place package in the current row
        if (self.x_filled + package.length <= self.length and
            self.last_plane_y + package.width <= self.width and
            self.last_filled_row_z + package.height <= self.height):
            self.packages[package.package_id] = package
            package.loaded = self.uld_id
            package_reference_corner = (self.x_filled, self.last_plane_y, self.last_filled_row_z)
            package.generate_corners(package_reference_corner)
            self.x_filled += package.length
            self.y_filled = max(self.last_plane_y + package.width, self.y_filled)
            self.z_filled = max(self.last_filled_row_z + package.height, self.z_filled)
            return True

        # Handle overflow to a new row or plane
        elif self.last_plane_y + package.width > self.width:
            return False
        elif (self.z_filled + package.height <= self.height and 
              self.x_filled + package.length > self.length):
            self.last_filled_row_z = self.z_filled
            self.x_filled = 0
            self.packages[package.package_id] = package
            package.loaded = self.uld_id
            package_reference_corner = (self.x_filled, self.last_plane_y, self.z_filled)
            package.generate_corners(package_reference_corner)
            self.x_filled = package.length
            self.y_filled = max(self.last_plane_y + package.width, self.y_filled)
            self.z_filled = self.last_filled_row_z + package.height
            return True
        elif self.y_filled + package.width <= self.width:
            self.last_plane_y = self.y_filled
            self.x_filled = 0
            self.z_filled = 0
            self.packages[package.package_id] = package
            package.loaded = self.uld_id
            package_reference_corner = (self.x_filled, self.last_plane_y, self.z_filled)
            package.generate_corners(package_reference_corner)
            self.x_filled = package.length
            self.y_filled = self.last_plane_y + package.width
            self.z_filled = package.height
            self.last_filled_row_z = 0
            return True
        else:
            return False

    def create_cuboid_environment(self):
        """
        Creates a cuboid representation of all loaded packages for spatial calculations.
        """
        self.existing_cuboids = [
            Cuboid(box_package.corners[0], box_package.corners[7])
            for box_package in self.packages.values()
        ]

    def fit_in_package(self, package):
        """
        Attempts to fit a package into the ULD by finding a suitable placement.

        Args:
            package (Package): The package to be placed.

        Returns:
            bool or str: ULD ID if the package is successfully placed, otherwise False.
        """
        larger_uld_cuboid = Cuboid((0, 0, 0), (self.length, self.width, self.height))
        possible_cuboid_dimensions = [
            (package.length, package.width, package.height),
            (package.width, package.length, package.height),
            (package.height, package.length, package.width),
            (package.height, package.width, package.length),
            (package.width, package.height, package.length),
            (package.length, package.height, package.width)
        ]
        for cuboid_dimension in possible_cuboid_dimensions:
            possible_placement = find_placement(cuboid_dimension, larger_uld_cuboid, self.existing_cuboids)
            if possible_placement:
                package.length, package.width, package.height = cuboid_dimension
                package_reference_corner = possible_placement
                package.generate_corners(package_reference_corner)
                self.packages[package.package_id] = package
                package.loaded = self.uld_id
                new_package_cuboid = Cuboid(package.corners[0], package.corners[7])
                self.existing_cuboids.append(new_package_cuboid)
                return package.loaded
        return False
