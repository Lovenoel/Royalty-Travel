import unittest
from unittest.mock import patch
from flask import url_for
from app import create_app, db

class WeatherEndpointTestCase(unittest.TestCase):

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
        """Test GET request with valid city parameter."""
        with self.app.test_request_context():
            response = self.client.get(url_for('weather.get_weather', city='London'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('main', response.json())  # Check if 'main' data is present in the response

    def test_missing_city_parameter(self):
        """Test GET request without providing the city parameter."""
        with self.app.test_request_context():
            response = self.client.get(url_for('weather.get_weather'))
            self.assertEqual(response.status_code, 400)
            self.assertIn('City parameter is required', response.json()['error'])

    @patch('requests.get')
    def test_non_200_status_code(self, mock_get):
        """Test handling of non-200 status code from OpenWeatherMap API."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.app.test_request_context():
            response = self.client.get(url_for('weather.get_weather', city='London'))
            self.assertEqual(response.status_code, 500)
            self.assertIn('Could not retrieve weather data', response.json()['error'])

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        """Test handling of connection error to OpenWeatherMap API."""
        mock_get.side_effect = ConnectionError('Connection failed')

        with self.app.test_request_context():
            response = self.client.get(url_for('weather.get_weather', city='London'))
            self.assertEqual(response.status_code, 500)
            self.assertIn('Could not retrieve weather data', response.json()['error'])

if __name__ == '__main__':
    unittest.main()

