import sys
import os
# sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + "/src")
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import unittest
from app import app
from mock import patch
from fakeredis import FakeStrictRedis
from rq import Queue

queue = Queue(is_async=False, connection=FakeStrictRedis())


@patch('app.q', queue)
class TestApp(unittest.TestCase):

    def setUp(self):
        app.config["Testing"] = True
        self.app = app.test_client()

    def test_reseize(self):
        params = dict(file=open("test.jpeg", 'rb'))
        url = "/resize"
        res = self.app.post(
            url, content_type='multipart/form-data', data=params, follow_redirects=True)

        self.assertEqual(res.status_code, 200)

    def test_get_result(self):
        url = "/resize/" + "test"
        res = self.app.get(url)

        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
