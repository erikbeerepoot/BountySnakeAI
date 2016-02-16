from bountysnakeai.tests import TestCase
from bountysnakeai import helper

class TestAStar(TestCase):

    def test_2x2(self):
        grid = [
            [
                helper.Node(1,(0,0)),
                helper.Node(1,(1,0)),
            ],
            [
                helper.Node(1,(0,1)),
                helper.Node(1,(1,1)),
            ],
        ]
        goal = helper.Node(1, (0,0))
        start = helper.Node(1, (1,1))
        result = helper.a_star(grid, goal, start)
        assert False # This test isn't quite right...
