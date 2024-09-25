"""
Bus Service
- Gets buses from database
- Gets their status
"""


class BusService:
    """Represents Bus Service"""
    def __init__(self, db):
        """Initializes the database
        Args:
            db: database
        """
        self.db = db

    def get_buses(self):
        """Gets Buses from databse"""
        return self.db["buses"]

    def get_bus_status(self, bus_id):
        """ Gets a Bus and its status
        Args:
            bus_id(int): bus' unique ID
        Returns:
            Bus status if found in database
            None if not found
        """
        for bus in self.db["buses"]:
            if bus["id"] == bus_id:
                return bus["status"]
        return None
