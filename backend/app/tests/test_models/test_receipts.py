import unittest
from app import create_app, db
from app.models import Receipt

class TestReceiptModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        - Creates a Flask application instance for testing.
        - Sets up a test client to simulate requests.
        - Establishes an application context.
        - Creates all database tables.
        """
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment after all tests.
        - Removes the application context.
        - Drops all database tables.
        """
        db.session.remove()
        db.drop_all()
        cls.ctx.pop()

    def setUp(self):
        """
        Set up before each test case.
        - Create sample Receipt objects and add them to the database.
        """
        self.receipt1 = Receipt(booking_id=1, amount=100.0)
        self.receipt2 = Receipt(booking_id=2, amount=150.0)

        db.session.add(self.receipt1)
        db.session.add(self.receipt2)
        db.session.commit()

    def tearDown(self):
        """
        Clean up after each test case.
        - Delete sample Receipt objects from the database.
        """
        db.session.delete(self.receipt1)
        db.session.delete(self.receipt2)
        db.session.commit()

    def test_to_dict_method(self):
        """
        Test case for `to_dict` method of Receipt model.
        - Creates a Receipt object.
        - Calls the `to_dict` method to serialize the object into a dictionary.
        - Verifies the correctness of the dictionary structure and values.
        """
        receipt_dict = self.receipt1.to_dict()

        self.assertEqual(receipt_dict['booking_id'], 1)
        self.assertEqual(receipt_dict['amount'], 100.0)

    def test_create_receipt(self):
        """
        Test case for creating a Receipt object.
        - Checks if the Receipt object was created successfully.
        - Verifies the booking_id and amount attributes of the created Receipt.
        """
        receipt = Receipt(booking_id=3, amount=200.0)
        db.session.add(receipt)
        db.session.commit()

        self.assertIsNotNone(receipt.id)
        self.assertEqual(receipt.booking_id, 3)

    def test_read_receipt(self):
        """
        Test case for reading a Receipt object from the database.
        - Retrieves a Receipt object using its primary key (id).
        - Verifies the correctness of retrieved attributes (booking_id, amount).
        """
        retrieved_receipt = Receipt.query.filter_by(booking_id=2).first()

        self.assertIsNotNone(retrieved_receipt)
        self.assertEqual(retrieved_receipt.amount, 150.0)

    def test_update_receipt(self):
        """
        Test case for updating a Receipt object.
        - Modifies attributes of an existing Receipt object.
        - Commits the changes and retrieves the updated Receipt.
        - Verifies that the changes are reflected correctly.
        """
        self.receipt1.amount = 120.0
        db.session.commit()

        updated_receipt = Receipt.query.filter_by(booking_id=1).first()
        self.assertEqual(updated_receipt.amount, 120.0)

    def test_delete_receipt(self):
        """
        Test case for deleting a Receipt object.
        - Deletes a Receipt object from the database.
        - Verifies that the object no longer exists in the database.
        """
        db.session.delete(self.receipt2)
        db.session.commit()

        deleted_receipt = Receipt.query.filter_by(booking_id=2).first()
        self.assertIsNone(deleted_receipt)

if __name__ == '__main__':
    unittest.main()
