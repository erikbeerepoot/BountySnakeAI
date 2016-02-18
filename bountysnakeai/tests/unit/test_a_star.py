import json

from bountysnakeai.tests import TestCase
from bountysnakeai import a_star
from bountysnakeai import model
from bountysnakeai.tests.unit import example_json

class TestAStar(TestCase):

    def test_2x2(self):
        Node = a_star.Node

        grid = [
            [
                Node(0,0),
                Node(0,1),
            ],
            [
                Node(1,0),
                Node(1,1),
            ],
        ]

        start = Node(0,0)
        goal = Node(1,1)

        path = a_star.find_path(grid, start, goal)

        # To get from position (0, 0) to position (W, H) on a grid, there are
        # (W+H choose W) equivalently good paths. Our algorithm is biased,
        # though, so we know it will always pick this one, in this case:
        self.assertEqual(path, [
            Node(0, 0),
            Node(0, 1),
            Node(1, 1),
        ])

    def test_build_grid(self):
        # FIXME: Super bad form to something like this in a unit test, but
        #        it's fastest to code right now...
        json_dict = json.loads(example_json.dummy_game)
        bs = model.BoardState(json_dict)

        grid = a_star.build_grid(bs.width, bs.height, bs.snake_list)

        Point = model.Point
        known_snake_positions = set([
            Point(1, 1), Point(1, 2), Point(2, 2), # snake 1
            Point(4, 4), Point(4, 3), Point(4, 2), Point(4, 1) # snake 2
        ])
        known_food_positions = set([
            Point(1, 2), Point(9, 3),
        ])

        for x in xrange(bs.width):
            for y in xrange(bs.height):
                node = grid[x][y]
                p = Point(x, y)
                if p in known_snake_positions:
                    self.assertEqual(node.contents, a_star.SNAKE)
                elif p in known_food_positions:
                    self.assertEqual(node.contents, a_star.FOOD)
                else:
                    self.assertEqual(node.contents, a_star.EMPTY)
