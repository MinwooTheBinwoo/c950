# Student ID: 011244239

import csv
from datetime import timedelta

from hashtable import HashTable
from package import Package
from truck import Truck
from distance import DistanceTable

# Reading and storing package information from csv into
# a hash table with the package_ID as the key.
def load_packages(filename):
    package_table = HashTable()

    with open(filename, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            package = Package(
                row[0],  # package ID
                row[1],  # address
                row[2],  # city
                row[4],  # zip
                row[5],  # deadline
                row[6],  # weight
                row[7],  # special note
                "At Hub"
            )

            package_table.insert(package.id, package)

    return package_table

# Creating the three trucks and loading them based on constraints
def load_trucks(package_table):
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)

    # Truck 1: early deadlines and grouped packages
    truck1_ids = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]

    # Truck 2: packages required to be on truck 2
    truck2_ids = [3, 18, 36, 38, 2, 4, 5, 7, 8, 10, 11, 12]

    # Truck 3: delayed packages and package 9 after address correction
    truck3_ids = [6, 9, 17, 21, 22, 23, 24, 25, 26, 27, 28, 32, 33, 35, 39]

    for package_id in truck1_ids:
        truck1.load(package_table, package_id)

    for package_id in truck2_ids:
        truck2.load(package_table, package_id)

    for package_id in truck3_ids:
        truck3.load(package_table, package_id)

    truck1.time = timedelta(hours=8)
    truck2.time = timedelta(hours=8)

    return truck1, truck2, truck3

# Updating package #9
def correct_package_9_address(package_table):
    package = package_table.lookup(9)
    package.address = "410 S State St"
    package.zip = "84111"
    package.status = "At Hub"

# Delivering packages using nearest neighbor algorithm
def deliver_route(truck, package_table, distance_table):
    while len(truck.packages) > 0:
        nearest_package_id = None
        nearest_distance = float("inf")

        for package_id in truck.packages:
            package = package_table.lookup(package_id)

            current_address_index = truck.current_location
            package_address_index = distance_table.get_address_index(package.address)

            distance = distance_table.get_distance(
                current_address_index,
                package_address_index
            )

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package_id = package_id

        package = package_table.lookup(nearest_package_id)
        next_location = distance_table.get_address_index(package.address)

        truck.deliver(package_table, nearest_package_id, nearest_distance)
        truck.current_location = next_location

# Calculating the mileage travelled by a truck up to the specified time
def mileage_at_time(truck, check_time):
    mileage = 0.0

    for entry in truck.delivery_history:
        if entry["time"] <= check_time:
            mileage += entry["distance"]

    return mileage


def format_time(time):
    total_seconds = int(time.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    suffix = "AM"
    if hours >= 12:
        suffix = "PM"

    display_hour = hours
    if display_hour > 12:
        display_hour -= 12

    return f"{display_hour}:{minutes:02d} {suffix}"

# Converting user input in HH:MM AM/PM format into a timedelta object
def parse_user_time(time_string):
    time_string = time_string.strip().upper()

    parts = time_string.split()

    if len(parts) != 2:
        return None

    clock_time = parts[0]
    period = parts[1]

    if period not in ["AM", "PM"]:
        return None

    hour_minute = clock_time.split(":")

    if len(hour_minute) != 2:
        return None

    hour = int(hour_minute[0])
    minute = int(hour_minute[1])

    if hour < 1 or hour > 12 or minute < 0 or minute > 59:
        return None

    if period == "PM" and hour != 12:
        hour += 12

    if period == "AM" and hour == 12:
        hour = 0

    return timedelta(hours=hour, minutes=minute)

# Determining the status of a package at the user-specified time
def get_package_status_at_time(package, check_time):
    if package.delivery_time is not None and check_time >= package.delivery_time:
        return "Delivered"

    if package.departure_time is not None and check_time >= package.departure_time:
        return "En Route"

    return "At Hub"

# Displaying the status and delivery info for one package
def print_package_status(package_table, package_id, check_time):
    package = package_table.lookup(package_id)

    if package is None:
        print("Package not found.")
        return

    status = get_package_status_at_time(package, check_time)

    print("\nPackage ID:", package.id)
    print("Address:", package.address)
    print("Deadline:", package.deadline)
    print("City:", package.city)
    print("ZIP:", package.zip)
    print("Weight:", package.weight)
    print("Truck:", package.loaded_truck_id)
    print("Status:", status)

    if package.delivery_time and check_time >= package.delivery_time:
        print("Delivery Time:", format_time(package.delivery_time))
    else:
        print("Delivery Time: TBD")

# Displaying the status of every package and the mileage travelled.
def print_all_package_statuses(package_table, check_time, truck1, truck2, truck3):
    for package_id in range(1, 41):
        package = package_table.lookup(package_id)
        status = get_package_status_at_time(package, check_time)

        if package.delivery_time and check_time >= package.delivery_time:
            delivery_time_display = format_time(package.delivery_time)
        else:
            delivery_time_display = "TBD"

        print(
            f"Package {package.id}: "
            f"{status}, "
            f"Truck {package.loaded_truck_id}, "
            f"Delivery Time: {delivery_time_display}"
        )

    truck1_mileage = mileage_at_time(truck1, check_time)
    truck2_mileage = mileage_at_time(truck2, check_time)
    truck3_mileage = mileage_at_time(truck3, check_time)

    total_mileage = truck1_mileage + truck2_mileage + truck3_mileage

    print("\n----------------------------------------")
    print(f"Truck 1 Mileage: {truck1_mileage:.2f} miles")
    print(f"Truck 2 Mileage: {truck2_mileage:.2f} miles")
    print(f"Truck 3 Mileage: {truck3_mileage:.2f} miles")
    print("----------------------------------------")
    print(f"Total Mileage: {total_mileage:.2f} miles")


def menu(package_table, truck1, truck2, truck3):
    while True:
        print("\nWGUPS Delivery System")
        print("1. View one package status")
        print("2. View all package statuses")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            package_id = int(input("Enter package ID: "))
            time_input = input("Enter time (HH:MM AM/PM): ")
            check_time = parse_user_time(time_input)

            if check_time is None:
                print("Error. Please try again.")

            print_package_status(package_table, package_id, check_time)

        elif choice == "2":
            time_input = input("Enter time (HH:MM AM/PM): ")
            check_time = parse_user_time(time_input)

            if check_time is None:
                print("Error. Please try again.")

            print_all_package_statuses(package_table, check_time, truck1, truck2, truck3)

        elif choice == "3":
            break

        else:
            print("Invalid option.")


def main():
    package_table = load_packages("info/packages.csv")
    distance_table = DistanceTable("info/addresses.csv", "info/distances.csv")

    truck1, truck2, truck3 = load_trucks(package_table)

    deliver_route(truck1, package_table, distance_table)
    deliver_route(truck2, package_table, distance_table)

    # Truck 3 can't leave unless a driver is available and package #9 is corrected.
    truck3.time = max(truck1.time, truck2.time, timedelta(hours=10, minutes=20))
    truck3.start_time = truck3.time

    correct_package_9_address(package_table)

    for package_id in truck1.original_packages:
        package = package_table.lookup(package_id)
        package.departure_time = truck1.start_time

    for package_id in truck2.original_packages:
        package = package_table.lookup(package_id)
        package.departure_time = truck2.start_time

    for package_id in truck3.original_packages:
        package = package_table.lookup(package_id)
        package.departure_time = truck3.start_time

    deliver_route(truck3, package_table, distance_table)

    menu(package_table, truck1, truck2, truck3)


if __name__ == "__main__":
    main()