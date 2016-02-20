import json

from bountysnakeai.tests import TestCase
from bountysnakeai import model
from bountysnakeai.tests.unit import example_json
from bountysnakeai import helper

class TestHelper(TestCase):

    def test_taunts(self):
	json_dict = json.loads(example_json.dummy_game)
        bs = model.BoardState(json_dict)

	taunt = helper.taunt_opponent(bs)
	assert(len(taunt)>0)


