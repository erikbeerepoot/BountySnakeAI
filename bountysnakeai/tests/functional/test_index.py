from bountysnakeai.tests import TestApp
from bountysnakeai.tests import TestCase
from bountysnakeai import main


class TestIndex(TestCase):
    def test_index(self):
        app = TestApp(main.application)
        response = app.get('/')
        assert response.status == '200 OK'
