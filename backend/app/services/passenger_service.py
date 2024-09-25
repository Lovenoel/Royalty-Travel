"""Passenger Service
- Creates a passenger
- Gets a passenger from database
- Gets a passenger by passenger_id
"""


class PassengerService:
    """Represents Passenger Service class"""

    def __init__(self, db):
        """Initializes a database
        Args:
            db: database
        """
        self.db = db

    def create_passenger(self, username, email, phoneNumber, contact_info):
        """ Creates a new passenger
        Args:
            username: name of the passenger
            email: email of the passenger
            phoneNumber: passenger's phone number
            contact_info: passenger's contact inform
        Returns:
            a new passenger and details
        """
        new_passenger = {
            "username": username,
            "email": email,
            "phoneNumber": phoneNumber,
            "contact_info": contact_info
        }
        self.db["passengers"].append(new_passenger)
        return new_passenger

    def get_passengers(self):
        """Gets a passenger from the database"""
        return self.db["passengers"]

    def get_passenger_by_id(self, passenger_id):
        """Gets a passenger by passenger_id
        Args:
            passenger_id: passengers' unique ID
        Returns:
            The passenger if found in database
            None if not found
        """
        for passenger in self.db["passengers"]:
            if passenger["id"] == passenger_id:
                return passenger
        return None
