import numpy as np

class Cuboid:
    def __init__(self, min_corner, max_corner):
        self.min_corner = min_corner 
        self.max_corner = max_corner

    def intersects(self, other):
        return not (
            self.max_corner[0] <= other.min_corner[0] or
            self.min_corner[0] >= other.max_corner[0] or
            self.max_corner[1] <= other.min_corner[1] or
            self.min_corner[1] >= other.max_corner[1] or
            self.max_corner[2] <= other.min_corner[2] or
            self.min_corner[2] >= other.max_corner[2]
        )

    def fits_inside(self, container):
        return all(
            self.min_corner[i] >= container.min_corner[i] and
            self.max_corner[i] <= container.max_corner[i]
            for i in range(3)
        )

    def place_at(self, origin, size):
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
    