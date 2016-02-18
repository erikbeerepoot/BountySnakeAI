import json

from bountysnakeai.tests import TestCase
from bountysnakeai import model
from bountysnakeai.tests.unit import example_json


class TestParsing(TestCase):

    def test_snake(self):
        json_dict = json.loads(example_json.dummy_snake_1)
        s = model.Snake(json_dict)

        self.assertEqual(s.id, "1234-567890-123456-7890")
        self.assertEqual(s.name, "The first snaaaake")
        self.assertEqual(s.status, "alive")
        self.assertEqual(s.message, "Moved north")
        self.assertEqual(s.taunt, "Let's rock!")
        self.assertEqual(s.age, 56)
        self.assertEqual(s.health, 83)
        self.assertEqual(s.coords, [
            model.Point(1, 1),
            model.Point(1, 2),
            model.Point(2, 2),
        ])
        self.assertEqual(s.kills, 4)
        self.assertEqual(s.food, 12)
        self.assertEqual(s.gold, 2)

    def test_boardstate(self):
        json_dict = json.loads(example_json.dummy_game)
        bs = model.BoardState(json_dict)

        self.assertEqual(bs.game, "hairy-cheese")
        self.assertEqual(bs.mode, "advanced")
        self.assertEqual(bs.turn, 4)
        self.assertEqual(bs.width, 30)
        self.assertEqual(bs.height, 20)
        self.assertEqual(len(bs.snake_list), 2)
        self.assertEqual(bs.snake_list[0].name, "The first snaaaake")
        self.assertEqual(bs.snake_list[1].name, "Another snaaaaake")
        self.assertEqual(bs.food_list, [
            model.Point(1, 5),
            model.Point(9, 3),
        ])
