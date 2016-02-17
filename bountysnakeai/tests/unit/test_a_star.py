from bountysnakeai.tests import TestCase
from bountysnakeai import helper

class TestAStar(TestCase):

    def test_2x2(self):
        start_point = helper.Point(0, 0)
        goal_point = helper.Point(1, 1)
        board = helper.build_board(2, 2, [], [])
        result = helper.a_star(board, start_point, goal_point)

        # To get from position (0, 0) to position (W, H) on a grid, there are
        # (W+H choose W) equivalently good paths. Our algorithm is biased,
        # though, so we know it will always pick this path, in this case:
        self.assertEqual(result, [
            helper.Point(0, 0),
            helper.Point(0, 1),
            helper.Point(1, 1),
        ])
