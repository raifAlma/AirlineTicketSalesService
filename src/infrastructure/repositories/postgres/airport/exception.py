

class AirportAlreadyExists(Exception):
    def __init__(self):
        super().__init__("Airport with this code already exists")