import random
from package import crainic_sorting
from genetic import GeneticAlgorithm

class OptimalCargoManagement(object):
    """
    A class to manage and optimize the loading of packages into Unit Load Devices (ULDs).

    Attributes:
        ulds (dict): A dictionary of ULDs, keyed by their unique IDs.
        packages (dict): A dictionary of packages, keyed by their unique IDs.
        K (float): Penalty cost for priority ULD activation.
        package_ordering (list): Combined ordering of priority and non-priority packages.
        non_priority_ordering (list): Ordering of non-priority packages.
        priority_ordering (list): Ordering of priority packages.
        verbose (bool): Whether to enable verbose logging.
    """

    def __init__(self, ulds, packages, K, verbose=False):
        """
        Initializes the OptimalCargoManagement instance.

        Args:
            ulds (dict): Dictionary of ULDs.
            packages (dict): Dictionary of packages.
            K (float): Penalty cost for priority ULD activation.
            verbose (bool, optional): Enables verbose logging if set to True. Default is False.
        """
        self.ulds = ulds
        self.packages = packages
        self.K = K
        self.package_ordering = None
        self.non_priority_ordering = None
        self.priority_ordering = None
        self.verbose = verbose

    def log(self, message):
        """
        Logs a message if verbose mode is enabled.

        Args:
            message (str): The message to log.
        """
        if self.verbose:
            print(message)

    def add_uld(self, uld):
        """
        Adds a new ULD to the system.

        Args:
            uld (ULD): The ULD object to add.
        """
        self.ulds[uld.uld_id] = uld

    def add_package(self, package):
        """
        Adds a new package to the system.

        Args:
            package (Package): The package object to add.
        """
        self.packages[package.package_id] = package

    def cost(self, only_priority=False):
        """
        Calculates the total cost of the solution, including priority and economy costs.

        Args:
            only_priority (bool, optional): If True, calculates only the priority cost. Default is False.

        Returns:
            float: The total cost of the solution.
        """
        priority_activated_ulds = set(
            package.loaded for package in self.packages.values() if package.priority and package.loaded
        )
        priority_cost = len(priority_activated_ulds)

        economy_cost = sum(
            package.delay for package in self.packages.values() if not package.priority and package.loaded is None
        )

        total_cost = priority_cost * self.K + economy_cost
        return priority_cost if only_priority else total_cost

    def num_packages_loaded(self):
        """
        Counts the number of packages successfully loaded into ULDs.

        Returns:
            int: Number of loaded packages.
        """
        return sum(1 for package in self.packages.values() if package.loaded is not None)

    def fit_greedy(self, optional_ordering=None, selected_ulds=None):
        """
        Attempts to load packages into ULDs using a greedy algorithm.

        Args:
            optional_ordering (list, optional): Custom ordering of packages for loading. Default is None.
            selected_ulds (list, optional): Specific ULD IDs to use for loading. Default is None.
        """
        self.log(f"Fitting packages: {len(self.packages)} packages in {len(self.ulds)} ULDs")
        self.log(f"Optional ordering: {True if optional_ordering is not None else False}")

        package_order = optional_ordering if optional_ordering else self.package_ordering
        for order in package_order:
            package_id = order[0]
            ulds_to_use = selected_ulds if selected_ulds else self.ulds.keys()
            for uld_id in ulds_to_use:
                if self.ulds[uld_id].uld_fill_greedy(self.packages[package_id]):
                    break

    def __repr__(self):
        """
        Returns a string representation of the OptimalCargoManagement instance.

        Returns:
            str: String representation of the instance.
        """
        uld_string = "Loaded ULDs:\n"
        for uld in self.ulds.values():
            if hasattr(uld, 'filled_coordinates') and uld.filled_coordinates:
                uld_string += f"{uld}\n"

        package_string = "Loaded Packages:\n"
        for package in self.packages.values():
            if package.loaded is not None:
                package_string += f"{package}\n"

        package_string += "Unloaded Packages:\n"
        for package in self.packages.values():
            if package.loaded is None:
                package_string += f"{package}\n"

        attributes = f"OptimalCargoManagement Attributes = {len(self.ulds)} ULDs, {len(self.packages)} Packages, K = {self.K}"
        return uld_string + package_string + attributes

    def file_output_ocm(self, filename):
        """
        Outputs the current solution to a file.

        Args:
            filename (str): Path to the output file.
        """
        with open(filename, 'w') as file:
            total_cost = self.cost()
            priority_cost = self.cost(only_priority=True)
            num_packages_loaded = self.num_packages_loaded()

            file.write(f"{total_cost},{num_packages_loaded},{priority_cost}\n")

            for package in self.packages.values():
                if package.loaded:
                    corners = package.corners
                    file.write(f"{package.package_id},{package.loaded},{corners[0][0]},{corners[0][1]},{corners[0][2]},{corners[7][0]},{corners[7][1]},{corners[7][2]}\n")
                else:
                    file.write(f"{package.package_id},NONE,-1,-1,-1,-1,-1,-1\n")

    def create_package_ordering(self):
        """
        Creates an optimized ordering of packages based on priority and dimensions.

        Returns:
            tuple: Priority ordering and non-priority ordering of packages.
        """
        priority_packages = [pkg for pkg in self.packages.values() if pkg.priority]
        non_priority_packages = [pkg for pkg in self.packages.values() if not pkg.priority]

        self.priority_ordering = crainic_sorting(priority_packages, group_on_dimensions=True, reverse=False)
        self.non_priority_ordering = crainic_sorting(non_priority_packages, group_on_dimensions=True)

        self.package_ordering = self.priority_ordering + self.non_priority_ordering
        self.log("Package Ordering Created\n")
        return self.priority_ordering, self.non_priority_ordering

        
    def reorient_packages(self):
        """
        Reorients packages based on their ordered Z-index orientations.

        This method adjusts the dimensions of each package in `self.package_ordering` 
        to match the specified orientation along the Z-axis.

        Modifies:
            Updates the dimensions of the packages to reflect the new orientation.
        """
        for order in self.package_ordering:
            package_id = order[0]
            order_z_against = order[1]            
            package_to_reorient = self.packages[package_id]
            package_to_reorient.reorient(order_z_against)

    def adhoc_additions(self, random_shuffle=False):
        """
        Attempts to load remaining unloaded packages into ULDs using an ad-hoc placement algorithm.

        Args:
            random_shuffle (bool, optional): If True, shuffles the list of unloaded packages before processing.
                Default is False.

        Modifies:
            Updates the loading status and placement of packages in `self.packages` and ULDs in `self.ulds`.
        """
        self.log(f"Performing Ad-Hoc Additions with Random Shuffle: {random_shuffle}")

        # Prepare the ULD environment
        for uld in self.ulds.values():
            uld.create_cuboid_environment()
        
        # Identify and sort unloaded packages
        unloaded_pkd_ids = [package.package_id for package in self.packages.values() if package.loaded is None]
        sorted_unloaded_pkd_ids = sorted(
            unloaded_pkd_ids,
            key=lambda x: self.packages[x].delay / max(self.packages[x].height, self.packages[x].width, self.packages[x].length),
            reverse=True
        )
        if random_shuffle:
            random.shuffle(sorted_unloaded_pkd_ids)

        # Try loading the sorted packages into ULDs
        adhoc_loaded_packages_count = 0
        for package_id in sorted_unloaded_pkd_ids:
            package = self.packages[package_id]
            for uld in self.ulds.values():
                if uld.fit_in_package(package):
                    adhoc_loaded_packages_count += 1
                    self.log(f"Package {package_id} loaded in ULD {uld.uld_id} via Ad-Hoc Addition")
                    break

        self.log(f"Ad-Hoc Additions Completed: {adhoc_loaded_packages_count} packages loaded")

    def unused_uld_ids(self):
        """
        Identifies the ULDs that are not used for loading any packages.

        Returns:
            set: A set of unused ULD IDs.
        """
        used_ulds = {package.loaded for package in self.packages.values() if package.loaded}
        unused_uld_ids = set(self.ulds.keys()) - used_ulds
        return unused_uld_ids

    def run_genetic_algorithm(self):
        """
        Optimizes the placement of priority and non-priority packages using a genetic algorithm.

        The method first processes priority packages into specific ULDs and then handles
        non-priority packages into remaining ULDs, ensuring optimized placement.

        Modifies:
            Updates the placement and orientation of both priority and non-priority packages 
            in `self.packages` and refreshes unused ULDs in `self.ulds`.

        Steps:
            1. Create and run a genetic algorithm instance for priority packages.
            2. Refresh unused ULDs and sort non-priority packages by economy score.
            3. Create and run a genetic algorithm instance for non-priority packages.
            4. Update ULDs and packages with the optimized placement.
        """
        # Process priority packages with genetic algorithm
        containers_data = [
            [uld.length, uld.width, uld.height, uld.uld_id]
            for uld in self.ulds.values() if uld.uld_id in ['U4', 'U5', 'U6']
        ]
        packages_data = [
            [package.length, package.width, package.height, package.package_id]
            for package in self.packages.values() if package.priority
        ]
        priority_ga_instance = GeneticAlgorithm(uld_dimensions=containers_data, package_dimensions=packages_data)
        priority_ga_solution = priority_ga_instance.run_genetic_algorithm()

        # Update placement of priority packages
        for package in self.packages.values():
            if package.priority:
                parent_uld = priority_ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = priority_ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = priority_ga_solution.get_package_orientation(package_id=package.package_id)
                package.loaded = parent_uld
                package.length, package.width, package.height = pkg_orientation
                package.generate_corners(ref_corner)

        # Refresh unused ULDs
        unused_uld_ids = self.unused_uld_ids()
        for uld_id in unused_uld_ids:
            self.ulds[uld_id].refresh()

        # Process non-priority packages
        non_priority_delay_dict = {pkg.package_id: pkg.delay for pkg in self.packages.values() if not pkg.priority}
        non_priority_volume_dict = {pkg.package_id: pkg.length * pkg.width * pkg.height for pkg in self.packages.values() if not pkg.priority}
        economy_pkg_ordering = sorted(
            self.non_priority_ordering,
            key=lambda x: (non_priority_delay_dict[x[0]]) / (non_priority_volume_dict[x[0]]) ** 1.2,
            reverse=True
        )[:150]
        economy_pkg_ordering = [pkg[0] for pkg in economy_pkg_ordering]
        random.shuffle(economy_pkg_ordering)

        eco_containers_data = [
            [uld.length, uld.width, uld.height, uld_id]
            for uld_id, uld in self.ulds.items() if uld_id in unused_uld_ids
        ]
        eco_packages_data = [
            [pkg.length, pkg.width, pkg.height, pkg.package_id]
            for pkg_id, pkg in self.packages.items() if pkg_id in economy_pkg_ordering
        ]
        economy_ga_instance = GeneticAlgorithm(uld_dimensions=eco_containers_data, package_dimensions=eco_packages_data)
        eco_ga_solution = economy_ga_instance.run_genetic_algorithm()

        # Update placement of non-priority packages
        for package in self.packages.values():
            if not package.priority and package.package_id in economy_pkg_ordering:
                if not eco_ga_solution.is_placed(package_id=package.package_id):
                    continue
                parent_uld = eco_ga_solution.get_parent_uld(package_id=package.package_id)
                ref_corner = eco_ga_solution.get_package_position(package_id=package.package_id)
                pkg_orientation = eco_ga_solution.get_package_orientation(package_id=package.package_id)
                package.loaded = parent_uld
                package.length, package.width, package.height = pkg_orientation
                package.generate_corners(ref_corner)

        # Update ULDs with loaded packages
        for package in self.packages.values():
            if package.loaded:
                self.ulds[package.loaded].add_package(package)

                    
            