from bountysnakeai.tests import TestCase
from bountysnakeai import helper

class TestAStar(TestCase):

    def test_2x2(self):
        Node = helper.Node

        grid = [
            [
                Node(1,(0,0)),
                Node(1,(0,1)),
            ],
            [
                Node(1,(1,0)),
                Node(1,(1,1)),
            ],
        ]

        start = Node(1, (1,1))
        goal = Node(1, (0,0))

        result = helper.a_star(grid, goal, start)

        # There are two valid paths to the goal and our algorithm is
        # non-deterministic, so check both!
        self.assertIn(result, [
            [
                Node(1, (1, 1)),
                Node(1, (1, 0)),
                Node(1, (0, 0)),
            ],
            [
                Node(1, (1, 1)),
                Node(1, (0, 1)),
                Node(1, (0, 0)),
            ],
        ])
