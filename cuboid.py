import numpy as np
import random

class Cuboid:
    """
    Represents a 3D cuboid defined by its minimum and maximum corners.

    Attributes:
        min_corner (tuple): Coordinates of the cuboid's minimum corner (x, y, z).
        max_corner (tuple): Coordinates of the cuboid's maximum corner (x, y, z).

    Methods:
        intersects(other): Checks if this cuboid intersects with another cuboid.
        fits_inside(container): Checks if this cuboid fits entirely inside another cuboid.
        place_at(origin, size): Places the cuboid at a specific origin with given dimensions.
        cuboid_corners(): Returns all eight corner points of the cuboid.
    """

    def __init__(self, min_corner, max_corner):
        """
        Initializes a Cuboid object with its minimum and maximum corners.

        Args:
            min_corner (tuple): Coordinates of the cuboid's minimum corner (x, y, z).
            max_corner (tuple): Coordinates of the cuboid's maximum corner (x, y, z).
        """
        self.min_corner = min_corner
        self.max_corner = max_corner

    def intersects(self, other):
        """
        Checks if this cuboid intersects with another cuboid.

        Args:
            other (Cuboid): Another Cuboid object.

        Returns:
            bool: True if the cuboids intersect, False otherwise.
        """
        return not (
            self.max_corner[0] <= other.min_corner[0] or
            self.min_corner[0] >= other.max_corner[0] or
            self.max_corner[1] <= other.min_corner[1] or
            self.min_corner[1] >= other.max_corner[1] or
            self.max_corner[2] <= other.min_corner[2] or
            self.min_corner[2] >= other.max_corner[2]
        )

    def fits_inside(self, container):
        """
        Checks if this cuboid fits entirely inside another cuboid.

        Args:
            container (Cuboid): The container Cuboid object.

        Returns:
            bool: True if this cuboid fits inside the container, False otherwise.
        """
        return all(
            self.min_corner[i] >= container.min_corner[i] and
            self.max_corner[i] <= container.max_corner[i]
            for i in range(3)
        )

    def place_at(self, origin, size):
        """
        Places the cuboid at a specific origin with given dimensions.

        Args:
            origin (tuple): The new origin (x, y, z) for the cuboid's minimum corner.
            size (tuple): Dimensions (length, width, height) of the cuboid.
        """
        self.min_corner = origin
        self.max_corner = tuple(origin[i] + size[i] for i in range(3))

    def cuboid_corners(self):
        """
        Returns all eight corner points of the cuboid.

        Returns:
            list: A list of tuples representing the eight corners of the cuboid.
        """
        height = self.max_corner[2] - self.min_corner[2]
        width = self.max_corner[1] - self.min_corner[1]
        length = self.max_corner[0] - self.min_corner[0]
        return [
            self.min_corner,
            (self.min_corner[0], self.min_corner[1], self.min_corner[2] + height),
            (self.min_corner[0], self.min_corner[1] + width, self.min_corner[2]),
            (self.min_corner[0], self.min_corner[1] + width, self.min_corner[2] + height),
            (self.min_corner[0] + length, self.min_corner[1], self.min_corner[2]),
            (self.min_corner[0] + length, self.min_corner[1], self.min_corner[2] + height),
            (self.min_corner[0] + length, self.min_corner[1] + width, self.min_corner[2]),
            self.max_corner
        ]

def find_placement(new_cuboid_size, larger_cuboid, existing_cuboids):
    """
    Finds a suitable placement for a new cuboid inside a larger cuboid without overlap.

    Args:
        new_cuboid_size (tuple): Dimensions (length, width, height) of the new cuboid.
        larger_cuboid (Cuboid): The larger cuboid container.
        existing_cuboids (list): List of existing Cuboid objects already placed inside the container.

    Returns:
        tuple or None: The origin (x, y, z) for placing the new cuboid if placement is possible, 
                       or None if no valid placement is found.
    """
    all_existing_corners = []
    for cuboid in existing_cuboids:
        all_existing_corners.extend(cuboid.cuboid_corners())

    possible_corners_output = []

    for possible_corner in all_existing_corners:
        possible_corners = [
            possible_corner,
            tuple(possible_corner[i] - new_cuboid_size[i] for i in range(3)),
            (possible_corner[0], possible_corner[1], possible_corner[2] - new_cuboid_size[2]),
            (possible_corner[0] - new_cuboid_size[0], possible_corner[1] - new_cuboid_size[1], possible_corner[2]),
            (possible_corner[0], possible_corner[1] - new_cuboid_size[1], possible_corner[2]),
            (possible_corner[0] - new_cuboid_size[0], possible_corner[1], possible_corner[2]),
            (possible_corner[0], possible_corner[1], possible_corner[2] - new_cuboid_size[2]),
            (possible_corner[0] - new_cuboid_size[0], possible_corner[1], possible_corner[2] - new_cuboid_size[2]),
        ]
        random.shuffle(possible_corners)

        for pc in possible_corners:
            new_cuboid = Cuboid(pc, tuple(pc[i] + new_cuboid_size[i] for i in range(3)))
            if not new_cuboid.fits_inside(larger_cuboid):
                continue
            for cuboid in existing_cuboids:
                if new_cuboid.intersects(cuboid):
                    break
            else:
                possible_corners_output.append(pc)

    if possible_corners_output:
        return possible_corners_output[np.random.randint(len(possible_corners_output))]
    else:
        return None
