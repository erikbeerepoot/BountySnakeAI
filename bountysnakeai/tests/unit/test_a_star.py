import json

from bountysnakeai.tests import TestCase
from bountysnakeai import a_star
from bountysnakeai import model
from bountysnakeai.tests.unit import example_json

class TestAStar(TestCase):

    def test_2x2_path(self):
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
        expected_path = [
            Node(0, 0),
            Node(0, 1),
            Node(1, 1),
        ]
        # To get from position (0, 0) to position (W, H) on a grid, there are
        # (W+H choose W) equivalently good paths. Our algorithm is biased,
        # though, so we know it will stick as close to the axes as possible:
        self.assertEqual(path, expected_path)

    def test_3x3_boxed_in(self):
        Node = a_star.Node
        SNAKE = a_star.SNAKE

        grid = [
            [
                Node(0,0, contents=SNAKE), # our snake
                Node(0,1, contents=SNAKE),
                Node(0,2),
            ],
            [
                Node(1,0, contents=SNAKE),
                Node(1,1, contents=SNAKE), # their snake
                Node(1,2),
            ],
            [
                Node(2,0),
                Node(2,1),
                Node(2,2),
            ],
        ]

        start = Node(0, 0)
        goal = Node(2, 2)

        with self.assertRaises(ValueError) as context:
            # We're stuck in a corner! This should throw an exception...
            path = a_star.find_path(grid, start, goal)

    def test_4x4_obstructed_path(self):
        Node = a_star.Node
        SNAKE = a_star.SNAKE
        grid = [
            [
                Node(0,0, contents=SNAKE), # our snake
                Node(0,1, contents=SNAKE),
                Node(0,2),
                Node(0,3),
            ],
            [
                Node(1,0),
                Node(1,1),
                Node(1,2),
                Node(1,3),
            ],
            [
                Node(2,0, contents=SNAKE),
                Node(2,1, contents=SNAKE),
                Node(2,2, contents=SNAKE), # their snake
                Node(2,3),
            ],
            [
                Node(3,0),
                Node(3,1),
                Node(3,2),
                Node(3,3),
            ],
        ]
        start = Node(0, 0)
        goal = Node(3, 2)
        path = a_star.find_path(grid, start, goal)
        expected_path = [
            Node(0, 0),
            Node(1, 0),
            Node(1, 1),
            Node(1, 2),
            Node(1, 3),
            Node(2, 3), # notice we have to go around the obstacle
            Node(3, 3), #
            Node(3, 2), # and then curve back
        ]
        self.assertEquals(path, expected_path)

    def test_build_grid(self):
        # FIXME: Super bad form to something like this in a unit test, but
        #        it's fastest to code right now...
        json_dict = json.loads(example_json.dummy_game)
        bs = model.BoardState(json_dict)

        grid = a_star.build_grid(bs.width, bs.height, bs.snake_list, bs.food_list)

        Point = model.Point
        known_snake_positions = set([
            Point(1, 1), Point(1, 2), Point(2, 2), # snake 1
            Point(4, 4), Point(4, 3), Point(4, 2), Point(4, 1) # snake 2
        ])
        known_food_positions = set([
            Point(1, 5), Point(9, 3),
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
