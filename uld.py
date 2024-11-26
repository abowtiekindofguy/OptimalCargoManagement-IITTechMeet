from package import Package

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
        # self.current_filled_row_z = 0
        
    def cost(self, K):
        for package_id, package in self.packages.items():
            if package.priority: return K
        return 0
    
    def add_package(self,package):
        self.packages[package.package_id]=package

    def remove_package(self,package_id):
        del self.packages[package_id]   

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
            