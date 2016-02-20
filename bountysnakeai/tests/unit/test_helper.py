import json
import copy
from bountysnakeai.tests import TestCase
from bountysnakeai import model
from bountysnakeai.tests.unit import example_json
from bountysnakeai import helper

class TestHelper(TestCase):

    def test_taunts(self):
	json_dict = json.loads(example_json.dummy_game)
        bs = model.BoardState(json_dict)

	taunt = helper.taunt_opponent(bs.snake_list)
	assert(len(taunt)>0)

    def test_dead_snakes_tester(self):
	json_dict = json.loads(example_json.dummy_game)
        bs = model.BoardState(json_dict)

	no_dead_snakes = helper.get_snakes_that_just_died(bs.snake_list,bs.snake_list)
	assert(not no_dead_snakes)

	snakes =  copy.deepcopy(bs.snake_list)
	snakes[0].status = "dead"
	one_dead_snake = helper.get_snakes_that_just_died(snakes,bs.snake_list)
	assert(len(one_dead_snake)==1)


