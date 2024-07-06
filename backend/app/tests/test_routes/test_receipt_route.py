import unittest
import json
from flask import Flask
from flask_testing import TestCase
from app import create_app, db
from app.models import Receipt

class ReceiptsBlueprintTestCase(TestCase):

    def create_app(self):
        """Create an instance of the Flask application for testing."""
        app = create_app('testing')
        return app

    def setUp(self):
        """Set up the test environment."""
        db.create_all()
        self.client.post('/login', data=dict(
            email='test@example.com',
            password='password123'
        ), follow_redirects=True)

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()

    def test_get_receipts_empty(self):
        """Test fetching receipts when the database is empty."""
        response = self.client.get('/receipt/receipts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [])

    def test_get_receipts_large_dataset(self):
        """Test fetching receipts with a large dataset."""
        # Create 1000 receipts
        for i in range(1000):
            receipt = Receipt(booking_id=i, amount=50.0, payment_method='credit_card')
            db.session.add(receipt)
        db.session.commit()

        response = self.client.get('/receipt/receipts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1000)

    def test_get_receipts_non_existent_endpoint(self):
        """Test accessing a non-existent endpoint under /receipts."""
        response = self.client.get('/receipt/receipts123')
        self.assertEqual(response.status_code, 404)

    def test_create_receipt_valid_input(self):
        """Test creating a receipt with valid input."""
        data = {
            'booking_id': 123,
            'amount': 50.0,
            'payment_method': 'credit_card'
        }
        response = self.client.post('/receipt/receipts', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['booking_id'], 123)

    def test_create_receipt_invalid_data_types(self):
        """Test creating a receipt with invalid data types."""
        data = {
            'booking_id': 'invalid_id',
            'amount': 'invalid_amount',
            'payment_method': 'invalid_method'
        }
        response = self.client.post('/receipt/receipts', json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_receipt_missing_field(self):
        """Test creating a receipt with a missing required field."""
        data = {
            'amount': 50.0,
            'payment_method': 'credit_card'
        }
        response = self.client.post('/receipt/receipts', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_receipt_by_id_valid_id(self):
        """Test fetching a receipt by valid ID."""
        receipt = Receipt(booking_id=123, amount=50.0, payment_method='credit_card')
        db.session.add(receipt)
        db.session.commit()

        response = self.client.get(f'/receipt/receipts/{receipt.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['booking_id'], 123)

    def test_get_receipt_by_id_non_existent_id(self):
        """Test fetching a receipt by non-existent ID."""
        response = self.client.get('/receipt/receipts/999')
        self.assertEqual(response.status_code, 404)

    def test_get_receipt_by_id_invalid_id_format(self):
        """Test fetching a receipt with invalid ID format."""
        response = self.client.get('/receipt/receipts/invalid_id')
        self.assertEqual(response.status_code, 400)

    def test_get_receipt_by_id_negative_id(self):
        """Test fetching a receipt with negative ID."""
        response = self.client.get('/receipt/receipts/-1')
        self.assertEqual(response.status_code, 400)

    def test_security_sql_injection(self):
        """Test for SQL injection attempt."""
        response = self.client.get("/receipt/receipts'; DROP TABLE receipts; --")
        self.assertEqual(response.status_code, 404)  # Assuming a safe response status for non-existent endpoint

if __name__ == '__main__':
    unittest.main()
