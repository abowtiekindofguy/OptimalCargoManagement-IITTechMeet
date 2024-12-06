class Coordinates:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return Coordinates(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Coordinates(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other):
        return Coordinates(self.x * other, self.y * other, self.z * other)
    def __truediv__(self, other):
        return Coordinates(self.x / other, self.y / other, self.z / other)
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __iter__(self):
        return iter([self.x, self.y, self.z])
    def __getitem__(self, index):
        return [self.x, self.y, self.z][index]
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Index out of range")
    def __len__(self):
        return 3
    def __copy__(self):
        return Coordinates(self.x, self.y, self.z)
    def __deepcopy__(self, memo):
        return Coordinates(self.x, self
        .y, self.z)
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5
    def to_tuple(self):
        return (self.x, self.y, self.z)
    def to_list(self):
        return [self.x, self.y, self.z]
    def to_dict(self):
        return {"x": self.x, "y": self.y, "z": self.z}
    @staticmethod
    def from_tuple(t):
        return Coordinates(t[0], t[1], t[2])
    @staticmethod
    def from_list(l):
        return Coordinates(l[0], l[1], l[2])
    @staticmethod
    def from_dict(d):
        return Coordinates(d["x"], d["y"], d["z"])
    def copy(self):
        return self.__copy__()
    def deepcopy(self):
        return self.__deepcopy__()
    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Coordinates(0, 0, 0)
        return self / mag
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    def x(self):
        return self.x
    def y(self):
        return self.y
    def z(self):
        return self.z
    def generate_cuboid_from_reference(self, x_max, y_max, z_max):
        assert x_max > 0 and y_max > 0 and z_max > 0
        return [Coordinates(self.x, self.y, self.z), Coordinates(self.x + x_max, self.y, self.z), Coordinates(self.x, self.y + y_max, self.z), Coordinates(self.x + x_max, self.y + y_max, self.z), Coordinates(self.x, self.y, self.z + z_max), Coordinates(self.x + x_max, self.y, self.z + z_max), Coordinates(self.x, self.y + y_max, self.z + z_max), Coordinates(self.x + x_max, self.y + y_max, self.z + z_max)]