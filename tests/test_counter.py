"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.client = app.test_client()
        self.client.testing = True


    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        # Make a call to Create a counter
        result = self.client.post('/counters/foo_update')
        # Ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # Check the counter value as a baseline
        baseline = result.get_json()['foo_update']
        # Make a call to Update the counter that you just created
        result = self.client.put('/counters/foo_update')
        # Ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the counter value is one more than the baseline you measured in step 3
        self.assertEqual(result.get_json()['foo_update'], baseline + 1)

    def test_read_a_counter(self):
        """It should read a counter"""
        # Create a counter
        result = self.client.post('/counters/foo_read')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # Read the counter
        result = self.client.get('/counters/foo_read')
        # Ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # Check that the counter value is correct
        self.assertEqual(result.get_json()['foo_read'], 0)

    def test_update_nonexistent_counter(self):
        """It should return an error for updating a nonexistent counter"""
        # Try to update a counter that does not exist
        result = self.client.put('/counters/nonexistent')
        # Ensure that it returned a 404 Not Found status code
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_nonexistent_counter(self):
        """It should return an error for reading a nonexistent counter"""
        # Try to read a counter that does not exist
        result = self.client.get('/counters/nonexistent')
        # Ensure that it returned a 404 Not Found status code
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_setUp(self):
        """It should set up a test client"""
        self.setUp()
        self.assertIsNotNone(self.client)

