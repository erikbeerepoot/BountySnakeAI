from bountysnakeai.tests import TestCase
from bountysnakeai import a_star

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
