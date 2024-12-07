from package import Package
from cuboid import *

class ULD:
    def __init__(self, uld_id, length, width, height, capacity):
        self.uld_id = uld_id
        self.length = length
        self.width = width
        self.height = height
        self.capacity = capacity 
        self.used_volume = 0
        self.used_weight = 0
        self.packages={}
        self.x_filled, self.y_filled, self.z_filled = 0, 0, 0
        self.last_plane_y = 0
        self.last_filled_row_z = 0
        self.existing_cuboids = []
        
    def cost(self, K):
        for package in self.packages.values():
            if package.priority: return K
        return 0
    
    def refresh(self):
        self.used_volume = 0
        self.used_weight = 0
        self.packages = {}
        self.x_filled, self.y_filled, self.z_filled = 0, 0, 0
        self.last_plane_y = 0
        self.last_filled_row_z = 0
        self.existing_cuboids = []
    
    def add_package(self,package):
        self.packages[package.package_id]=package

    def __repr__(self):
        return f"ULD({self.uld_id}, {self.length}, {self.width}, {self.height}, {self.capacity})"

    def update_filled_coordinates(self, package):
        if self.x_filled + package.length <= self.length and self.last_plane_y + package.width <= self.width and self.last_filled_row_z + package.height <= self.height:
            self.packages[package.package_id]=package
            package.loaded = self.uld_id
            package_reference_corner = (self.x_filled, self.last_plane_y, self.last_filled_row_z)
            package.generate_corners(package_reference_corner)
            self.x_filled = self.x_filled + package.length
            self.y_filled = max(self.last_plane_y + package.width, self.y_filled) 
            self.z_filled = max(self.last_filled_row_z + package.height, self.z_filled)
            return True
        
        elif self.last_plane_y + package.width > self.width:
            return False
        
        elif self.z_filled + package.height <= self.height and self.x_filled + package.length > self.length:      
            self.last_filled_row_z = self.z_filled 
            self.x_filled = 0
            
            self.packages[package.package_id]=package   
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
            self.packages[package.package_id]=package
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
        self.existing_cuboids = []
        for package_id, box_package in self.packages.items():
            package_cuboid = Cuboid(box_package.corners[0], box_package.corners[7])
            # package_corners = package_cuboid.cuboid_corners()
            # self.existing_cuboid_corners.extend(package_corners)
            self.existing_cuboids.append(package_cuboid)
            
    def fit_in_package(self, package):
        larger_uld_cuboid = Cuboid((0, 0, 0), (self.length, self.width, self.height))
        possible_cuboid_dimensions = [(package.length, package.width, package.height), (package.width, package.length, package.height), (package.height, package.length, package.width), (package.height, package.width, package.length), (package.width, package.height, package.length), (package.length, package.height, package.width)]
        for cuboid_dimension in possible_cuboid_dimensions:
            possible_placement = find_placement(cuboid_dimension, larger_uld_cuboid, self.existing_cuboids)
            if possible_placement:
                package.length, package.width, package.height = cuboid_dimension
                package_reference_corner = possible_placement
                package.generate_corners(package_reference_corner)
                self.packages[package.package_id]=package
                package.loaded = self.uld_id
                new_package_cuboid = Cuboid(package.corners[0], package.corners[7])
                # self.existing_cuboid_corners.extend(new_package_cuboid.cuboid_corners())
                self.existing_cuboids.append(new_package_cuboid)
                return package.loaded
        return False
        