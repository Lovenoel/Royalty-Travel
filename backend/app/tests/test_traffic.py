import unittest
from unittest.mock import patch
from flask import url_for
from app import create_app, db

class TrafficEndpointTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_valid_request(self):
        """Test GET request with valid origin and destination."""
        with self.app.test_request_context():
            response = self.client.get(url_for('traffic.get_traffic', origin='New+York', destination='Los+Angeles'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('route', response.json())  # Check if route information is present in the response

    def test_missing_parameters(self):
        """Test GET request with missing origin or destination."""
        with self.app.test_request_context():
            response = self.client.get(url_for('traffic.get_traffic'))
            self.assertEqual(response.status_code, 400)
            self.assertIn('Origin and destination parameters are required', response.json()['error'])

    @patch('requests.get')
    def test_non_200_status_code(self, mock_get):
        """Test handling of non-200 status code from TomTom API."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.app.test_request_context():
            response = self.client.get(url_for('traffic.get_traffic', origin='New+York', destination='Los+Angeles'))
            self.assertEqual(response.status_code, 500)
            self.assertIn('Could not retrieve traffic data', response.json()['error'])

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        """Test handling of connection error to TomTom API."""
        mock_get.side_effect = ConnectionError('Connection failed')

        with self.app.test_request_context():
            response = self.client.get(url_for('traffic.get_traffic', origin='New+York', destination='Los+Angeles'))
            self.assertEqual(response.status_code, 500)
            self.assertIn('Could not retrieve traffic data', response.json()['error'])

if __name__ == '__main__':
    unittest.main()

