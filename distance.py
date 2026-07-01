import csv


class DistanceTable:
    def __init__(self, address_file, distance_file):
        self.location_names = []
        self.addresses = []
        self.distances = []

        self.load_addresses(address_file)
        self.load_distances(distance_file)

    def load_addresses(self, address_file):
        with open(address_file, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)

            for row in reader:
                self.location_names.append(row[0])
                self.addresses.append(row[1])

    def load_distances(self, distance_file):
        with open(distance_file, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)

            for row in reader:
                distance_row = []

                for value in row:
                    if value == "":
                        distance_row.append(None)
                    else:
                        distance_row.append(float(value))

                self.distances.append(distance_row)

    def get_address_index(self, address):
        address = address.lower().strip()

        for i in range(len(self.addresses)):
            if self.addresses[i].lower().strip() == address:
                return i

        return None

    def get_distance(self, index_1, index_2):
        distance = self.distances[index_1][index_2]

        if distance is None:
            distance = self.distances[index_2][index_1]

        return distance