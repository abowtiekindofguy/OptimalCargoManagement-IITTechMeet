from package import Package
from uld import ULD
from cuboid import Cuboid

class SolutionValidator:
    """
    A class to validate the solution of package loading into ULDs (Unit Load Devices) and calculate various scores.

    Attributes:
        solution (object): The solution object containing packages and ULDs.
        verbose (bool): Enables verbose logging if set to True.
        valid (bool): Indicates if the solution is valid.
        package_collection (dict): A dictionary mapping ULD IDs to the list of packages assigned to each ULD.

    Methods:
        log(message): Logs a message if verbose is enabled.
        validate_uld(uld, packages): Validates a single ULD and checks that all packages fit inside without overlap.
        validate(): Validates all ULDs in the solution, ensuring package constraints are met.
        is_valid(): Returns the validity status of the solution.
        priority_score(): Calculates the priority score of the solution based on priority packages in ULDs.
        economy_score(): Calculates the economy score based on the delays of unallocated packages.
        total_score(): Computes the total score as the sum of the priority and economy scores.
    """

    def __init__(self, solution, verbose=False):
        """
        Initializes the SolutionValidator instance.

        Args:
            solution (object): The solution object containing packages and ULDs.
            verbose (bool, optional): Enables verbose logging if set to True. Default is False.
        """
        self.solution_packages = solution.packages
        self.solution_ulds = solution.ulds
        self.valid = False
        self.package_collection = None
        self.verbose = verbose

    def log(self, message):
        """
        Logs a message if verbose is enabled.

        Args:
            message (str): The message to log.
        """
        if self.verbose:
            print(message)

    def validate_uld(self, uld, packages):
        """
        Validates a single ULD, ensuring all packages fit inside without overlap.

        Args:
            uld (ULD): The ULD object to validate.
            packages (list): A list of Package objects to validate within the ULD.

        Returns:
            bool: True if the ULD is valid, False otherwise.
        """
        uld_cuboid = Cuboid((0, 0, 0), (uld.length, uld.width, uld.height))
        package_cuboid_list = []

        for package in packages:
            package_cuboid = Cuboid(package.corners[0], package.corners[7])
            package_cuboid_list.append(package_cuboid)

        for i in range(len(package_cuboid_list)):
            if not package_cuboid_list[i].fits_inside(uld_cuboid):
                self.log(f"Package {i} does not fit inside ULD {uld_cuboid}")
                self.log(package_cuboid_list[i])
                return False

            for j in range(i + 1, len(package_cuboid_list)):
                if package_cuboid_list[i].intersects(package_cuboid_list[j]):
                    self.log(f"Package {i} intersects with Package {j}")
                    self.log(f"{package_cuboid_list[i]}\n{package_cuboid_list[j]}")
                    return False

        return True

    def validate(self):
        """
        Validates all ULDs in the solution, ensuring package constraints are met.
        Also checks maximum weight constraints for each ULD.

        Returns:
            None
        """
        package_collection = {uld_id: [] for uld_id in self.solution_ulds}
        self.package_collection = package_collection

        for package_id, package in self.solution_packages.items():
            if package.loaded:
                package_collection[package.loaded].append(package)

        for uld_id in package_collection:
            uld = self.solution_ulds[uld_id]
            self.log(f"Validating ULD {uld_id}")
            validate_uld_bool = self.validate_uld(uld, package_collection[uld_id])
            if not validate_uld_bool:
                self.valid = False
                self.log(f"ULD {uld_id} is invalid")
                return

            self.log(f"ULD {uld_id} is valid")

        self.log("Checking Max Weight Constraints")
        for uld_id in package_collection:
            uld = self.solution_ulds[uld_id]
            uld_max_weight = uld.capacity
            package_weight = sum([package.weight for package in package_collection[uld_id]])
            if package_weight > uld_max_weight:
                self.valid = False
                self.log(f"ULD {uld_id} exceeds max weight")
                return

        self.log("All Constraints Satisfied!!")
        self.valid = True
        return

    def is_valid(self):
        """
        Returns the validity status of the solution.

        Returns:
            bool: True if the solution is valid, False otherwise.
        """
        return self.valid

    def priority_score(self):
        """
        Calculates the priority score of the solution based on priority packages in ULDs.

        Returns:
            int: The priority score.
        """
        assert self.valid, "Solution is not valid"
        assert self.package_collection is not None, "Solution is not validated"

        priority_score = 0

        for uld_id in self.package_collection:
            uld_priority_score = 0
            for package in self.package_collection[uld_id]:
                if package.priority:
                    uld_priority_score = 1
                    break
            priority_score += uld_priority_score

        return priority_score

    def economy_score(self):
        """
        Calculates the economy score based on the delays of unallocated packages.

        Returns:
            int: The economy score.
        """
        assert self.valid, "Solution is not valid"
        assert self.package_collection is not None, "Solution is not validated"

        delay_score = 0

        for package in self.solution_packages.values():
            if package.loaded is None:
                delay_score += package.delay

        return delay_score

    def total_score(self):
        """
        Computes the total score as the sum of the priority and economy scores.

        Returns:
            int: The total score.
        """
        assert self.valid, "Solution is not valid"
        assert self.package_collection is not None, "Solution is not validated"

        economy_score, priority_score = self.economy_score(), self.priority_score()

        return economy_score + priority_score
