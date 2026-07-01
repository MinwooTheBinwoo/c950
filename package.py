class Package:
    def __init__(self, id, address, city, zip_code, deadline, weight, special_note, status):
        self.id = int(id)
        self.address = address
        self.city = city
        self.zip = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.status = status
        self.departure_time = None
        self.loaded_truck_id = None

        self.special_note_lower = self.special_note.lower() # Getting rid of case sensitivity

        # Default status logic
        if "delayed" in self.special_note_lower:
            self.status = "Delayed"
        elif "wrong address" in self.special_note_lower:
            self.status = "Address Issue"
        else:
            self.status = "At hub"

        self.delivery_time = None

        # Constraints
        self.required_truck = None
        self.package_must_be_with = []

        self.parse_notes()

    def parse_notes(self):
        special_note_lower = self.special_note.lower() # Getting rid of case sensitivity

        # Truck Requirements
        if "truck 2" in self.special_note_lower:
            self.required_truck = 2

        # Packages that must be delivered together
        if "must be delivered with" in self.special_note_lower:
            # Grabbing numbers from string
            delimited_note = self.special_note.replace (",", " ")
            words = delimited_note.split()

            for word in words:
                if word.isdigit():
                    self.package_must_be_with.append(int(word))
