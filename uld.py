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
        
    def cost(self, K):
        for package_id, package in self.packages.items:
            if package.priority: return K
        return 0
    
    def add_package(self,package):
        self.packages[package.package_id]=package

    def remove_package(self,package_id):
        del self.packages[package_id]   

    def __repr__(self):
        return f"ULD({self.uld_id}, {self.length}, {self.width}, {self.height}, {self.capacity})"
