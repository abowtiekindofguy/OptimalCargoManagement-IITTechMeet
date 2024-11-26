class Package:
    def __init__(self, package_id, length, width, height, weight, priority, delay):
        self.package_id = package_id
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.priority = 1 if priority == "Priority" else 0
        self.delay = delay
        self.corners = []
        self.loaded = None
        
    # def reference_corner(self):
    #     self.corners
    
    def center(self):
        x_center, y_center, z_center = 0, 0, 0
        for corner in self.corners:
            x_center += corner[0]
            y_center += corner[1]
            z_center += corner[2]
        x_center /= 8
        y_center /= 8
        z_center /= 8
        return x_center, y_center, z_center
        
        
    def __repr__(self):
        return f"Package({self.package_id}, {self.length}, {self.width}, {self.height}, {self.weight}, {self.priority}, {self.delay})"

