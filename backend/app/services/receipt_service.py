"""
Receipt Service
- Creates receipts
- Gets receipts from database with its unique ID
"""

class ReceiptService:
    """Service class for handling receipts."""

    def __init__(self, db):
        """
        Initializes the ReceiptService with a database.

        Args:
            db (dict): Database dictionary containing 'receipts' list.
        """
        self.db = db

    def create_receipt(self, booking_id, amount, payment_method):
        """
        Creates a new receipt and adds it to the database.

        Args:
            booking_id (int): Booking ID associated with the receipt.
            amount (int): Amount of the transport fare.
            payment_method (str): Method of payment used.

        Returns:
            dict: New receipt created.
        """
        new_receipt = {
            "booking_id": booking_id,
            "amount": amount,
            "payment_method": payment_method
        }
        self.db["receipts"].append(new_receipt)
        return new_receipt

    def get_receipts(self):
        """
        Retrieves all receipts from the database.

        Returns:
            list: List of all receipts in the database.
        """
        return self.db["receipts"]

    def get_receipt_by_id(self, receipt_id):
        """
        Retrieves a receipt by its unique ID from the database.

        Args:
            receipt_id (int): Unique ID of the receipt.

        Returns:
            dict or None: Receipt if found, None if not found.
        """
        for receipt in self.db["receipts"]:
            if receipt["id"] == receipt_id:
                return receipt
        return None

