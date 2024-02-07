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
from src.counter import app
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
        result = self.client.post('/counters/foo_update')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        baseline = result.get_json()['foo_update']
        result = self.client.put('/counters/foo_update')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_json()['foo_update'], baseline + 1)

    def test_read_a_counter(self):
        """It should read a counter"""
        result = self.client.post('/counters/foo_read')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.get('/counters/foo_read')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_json()['foo_read'], 0)

    def test_update_nonexistent_counter(self):
        """It should return an error for updating a nonexistent counter"""
        result = self.client.put('/counters/nonexistent')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_nonexistent_counter(self):
        """It should return an error for reading a nonexistent counter"""
        result = self.client.get('/counters/nonexistent')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        result = self.client.post('/counters/foo_delete')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.delete('/counters/foo_delete')
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        result = self.client.get('/counters/foo_delete')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_counter(self):
        """It should return 404 for non-existent counter"""
        result = self.client.delete('/counters/non_existent_counter')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_setUp(self):
        self.setUp()
        self.assertIsNotNone(self.client)
