# import numpy as np

# class Cuboid:
#     def __init__(self, min_corner, max_corner):
#         self.min_corner = min_corner 
#         self.max_corner = max_corner

#     def intersects(self, other):
#         return not (
#             self.max_corner[0] <= other.min_corner[0] or
#             self.min_corner[0] >= other.max_corner[0] or
#             self.max_corner[1] <= other.min_corner[1] or
#             self.min_corner[1] >= other.max_corner[1] or
#             self.max_corner[2] <= other.min_corner[2] or
#             self.min_corner[2] >= other.max_corner[2]
#         )

#     def fits_inside(self, other):
#         return all(
#             self.min_corner[i] >= other.min_corner[i] and
#             self.max_corner[i] <= other.max_corner[i]
#             for i in range(3)
#         )

#     def place_at(self, origin, size):
#         self.min_corner = origin
#         self.max_corner = tuple(origin[i] + size[i] for i in range(3))
        
#     def cuboid_corners(self):
#         height = self.max_corner[2] - self.min_corner[2]
#         width = self.max_corner[1] - self.min_corner[1]
#         length = self.max_corner[0] - self.min_corner[0]
#         return [
#             self.min_corner,
#             (self.min_corner[0], self.min_corner[1], self.min_corner[2] + height),
#             (self.min_corner[0], self.min_corner[1] + width, self.min_corner[2]),
#             (self.min_corner[0], self.min_corner[1] + width, self.min_corner[2] + height),
#             (self.min_corner[0] + length, self.min_corner[1], self.min_corner[2]),
#             (self.min_corner[0] + length, self.min_corner[1], self.min_corner[2] + height),
#             (self.min_corner[0] + length, self.min_corner[1] + width, self.min_corner[2]),
#             self.max_corner
#         ]
#     def __repr__(self):
#         return f"Cuboid({self.min_corner}, {self.max_corner})"

# def find_placement(new_cuboid_size, larger_cuboid, existing_cuboid_corners):
#     possible_corners = []
#     for possible_corner in existing_cuboid_corners:
#         new_cuboid = Cuboid(possible_corner, tuple(possible_corner[i] + new_cuboid_size[i] for i in range(3)))
#         if not new_cuboid.fits_inside(larger_cuboid):
#             continue
#         for cuboid in existing_cuboid_corners:
#             if new_cuboid.intersects(cuboid):
#                 break
#         else:
#             possible_corners.append(possible_corner)
            
#     if possible_corners:
#         return possible_corners[np.random.randint(len(possible_corners))]
#     else:
#         return None
    
    
import numpy as np

class Cuboid:
    def __init__(self, min_corner, max_corner):
        self.min_corner = min_corner 
        self.max_corner = max_corner

    def intersects(self, other):
        """Check if this cuboid intersects with another cuboid."""
        return not (
            self.max_corner[0] <= other.min_corner[0] or
            self.min_corner[0] >= other.max_corner[0] or
            self.max_corner[1] <= other.min_corner[1] or
            self.min_corner[1] >= other.max_corner[1] or
            self.max_corner[2] <= other.min_corner[2] or
            self.min_corner[2] >= other.max_corner[2]
        )

    def fits_inside(self, container):
        """Check if this cuboid fits completely inside another cuboid."""
        return all(
            self.min_corner[i] >= container.min_corner[i] and
            self.max_corner[i] <= container.max_corner[i]
            for i in range(3)
        )

    def place_at(self, origin, size):
        """Update the cuboid's position based on origin and size."""
        self.min_corner = origin
        self.max_corner = tuple(origin[i] + size[i] for i in range(3))
        
    def cuboid_corners(self):
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


def find_free_spaces(larger_cuboid, existing_cuboids):
    """Generate free spaces as a list of cuboids."""
    free_spaces = [larger_cuboid]

    for cuboid in existing_cuboids:
        new_free_spaces = []
        for free_space in free_spaces:
            # Split free_space into smaller regions excluding the occupied cuboid
            new_free_spaces.extend(split_free_space(free_space, cuboid))
        free_spaces = new_free_spaces

    return free_spaces

def split_free_space(free_space, occupied_cuboid):
    """Split free space into smaller cuboids that do not overlap with the occupied cuboid."""
    result = []

    # Only keep non-overlapping subregions
    if not free_space.intersects(occupied_cuboid):
        result.append(free_space)
    else:
        for dim in range(3):  # Split along x, y, z axes
            if free_space.min_corner[dim] < occupied_cuboid.min_corner[dim]:
                sub_cuboid = Cuboid(
                    free_space.min_corner,
                    tuple(
                        min(free_space.max_corner[d], occupied_cuboid.min_corner[d]) if d == dim else free_space.max_corner[d]
                        for d in range(3)
                    )
                )
                result.append(sub_cuboid)
            if free_space.max_corner[dim] > occupied_cuboid.max_corner[dim]:
                sub_cuboid = Cuboid(
                    tuple(
                        max(free_space.min_corner[d], occupied_cuboid.max_corner[d]) if d == dim else free_space.min_corner[d]
                        for d in range(3)
                    ),
                    free_space.max_corner
                )
                result.append(sub_cuboid)

    return result



# def find_placement(new_cuboid_size, larger_cuboid, existing_cuboids):
#     free_spaces = find_free_spaces(larger_cuboid, existing_cuboids)
#     new_cuboid = Cuboid((0, 0, 0), new_cuboid_size)

#     for free_space in free_spaces:
#         # Check if the new cuboid can fit inside this free space
#         for dim in range(3):
#             start = free_space.min_corner[dim]
#             end = free_space.max_corner[dim] - new_cuboid_size[dim]
#             if start > end:
#                 break
#         else:
#             # Found a free space where the new cuboid can fit
#             return free_space.min_corner

#     return None

def find_placement(new_cuboid_size, larger_cuboid, existing_cuboids):
    all_existing_corners = []
    for cuboid in existing_cuboids:
        all_existing_corners.extend(cuboid.cuboid_corners())
    possible_corners = []
    for possible_corner in all_existing_corners:
        new_cuboid = Cuboid(possible_corner, tuple(possible_corner[i] + new_cuboid_size[i] for i in range(3)))
        if not new_cuboid.fits_inside(larger_cuboid):
            continue
        for cuboid in existing_cuboids:
            if new_cuboid.intersects(cuboid):
                break
        else:
            possible_corners.append(possible_corner)
            
    if possible_corners:
        return possible_corners[np.random.randint(len(possible_corners))]
    else:
        return None
    