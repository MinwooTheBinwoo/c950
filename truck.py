from datetime import timedelta


class Truck:
    def __init__(self, truck_id, capacity=16, speed=18):
        self.id = truck_id
        self.capacity = capacity
        self.speed = speed  # in miles per hour
        self.packages = [] # using the package IDs
        self.original_packages = [] # package manifest
        self.driver_id = None
        self.current_location = 0
        self.mileage = 0.0
        self.delivery_history = []
        self.time = timedelta(hours=8) # Truck starts at 8:00 AM
        self.start_time = self.time

    # Loading a package onto the truck
    def load(self, ht, package_id):
        if len(self.packages) >= self.capacity:
            return False

        package = ht.lookup(package_id)

        if package is None:
            return False

        self.packages.append(package_id)
        self.original_packages.append(package_id)
        package.loaded_truck_id = self.id

        # Only update status if the package is actually at the hub.
        # Delayed or address issue packages should keep their initial status.
        if package.status == "At Hub":
            package.status = "En Route"

        return True

    # Delivering the package
    def deliver(self, ht, package_id, distance):
        # Checking if the package is actually on the truck
        if package_id not in self.packages:
            return False

        # Looking up package in the hash table
        package = ht.lookup(package_id)

        if package is None:
            return False

        self.packages.remove(package_id)
        self.mileage += distance
        travel_time = timedelta(hours=distance / self.speed)
        self.time += travel_time

        # Saving the delivery segment
        self.delivery_history.append({
            "package_id": package_id,
            "distance": distance,
            "time": self.time
        })
        
        package.status = "Delivered"
        package.delivery_time = self.time

        return True

    # Assigning a driver
    def assign_driver(self, driver_id):
        self.driver_id = driver_id

    # Checking if the truck is full
    def is_full(self):
        return len(self.packages) >= self.capacity

    # Number of packages onboard
    def package_count(self):
        return len(self.packages)

    # Displaying truck information
    def __str__(self):
        return (
            f"Truck {self.id}\n"
            f"Driver: {self.driver_id}\n"
            f"Packages: {self.packages}\n"
            f"Mileage: {self.mileage}\n"
            f"Current Time: {self.time}"
        )