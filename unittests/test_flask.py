import unittest
import requests
import app


class TestFlask(unittest.TestCase):
    the_app = app.app
    ossi_host = 'http://localhost:5000'

    def test_hello_message(self):
        response = requests.get(self.ossi_host)
        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertIsNotNone(body)
        self.assertEqual("Hi I'm OSSI! The [OSS] L[I]cense Checker!", body['message'])

    def test_license_string_search(self):
        url = f"{self.ossi_host}/licenses/mit"
        response = requests.get(url)
        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertEqual(11, len(body))
        expected = "MIT license / X11 license"
        self.assertEqual(expected, body['License'])
        expected = "MIT"
        self.assertEqual(expected, body['Author'])

    def test_get_all_license(self):
        url = f"{self.ossi_host}/licenses"
        response = requests.get(url)
        self.assertEqual(200, response.status_code)
        body = response.json()
        self.assertEqual(39, len(body))