import json

from bountysnakeai.tests import TestApp
from bountysnakeai.tests import TestCase
from bountysnakeai import main


class TestIndex(TestCase):
    def test_index(self):
        app = TestApp(main.application)
        response = app.get('/')
        self.assertEqual(response.status, '200 OK')
        json_body = json.loads(response.body)
        self.assertEqual(json_body, {
            'color': '#3398CC',
            'head': 'http://localhost:80/static/head.png',
        })
        # TODO: Update this test to use a non-default scheme (HTTPS vs HTTP)
        #       and domain (e.g. not localhost:80)
