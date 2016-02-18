import json

from bountysnakeai.tests import ControllerTestCase
from bountysnakeai.tests import TestApp
from bountysnakeai import main

start_game_json = {
    u'game': u'test-game',
    u'mode': u'classic',
    u'turn': 0,
    u'board': {
        u'height': 20,
        u'width': 20,
    },
    u'snakes': [],
    u'food': [],
    # Advanced mode only:
    # u'walls': [],
    # u'gold': [],
}

start_snakes_json = [
    {
        'id': 'our-snake-id',
        'name': 'our snake',
        'status': 'alive',
        'message': 'Moved north',
        'taunt': 'Let\'s rock!',
        'age': 56,
        'health': 83,
        'coords': [ [1, 1], [1, 2], [2, 2] ],
        'kills': 4,
        'food': 12,
        'gold': 2
    },
    {
        'id': 'their-snake-id',
        'name': 'the enemy snake',
        'status': 'alive',
        'message': 'Moved south',
        'taunt': 'Let\'s roll!',
        'age': 56,
        'health': 83,
        'coords': [ [4, 2], [4, 3], [4, 4] ],
        'kills': 5,
        'food': 10,
        'gold': 2
    }
]

class TestGame(ControllerTestCase):
    def setUp(self):
        super(TestGame, self).setUp()
        self.old_snake_id = main.snakeID
        main.snakeID = 'our-snake-id'

    def tearDown(self):
        super(TestGame, self).tearDown()
        main.snakeID = self.old_snake_id

    def test_start(self):
        app = TestApp(main.application)
        json_dict = start_game_json.copy()
        json_dict[u'snakes'] = [d.copy() for d in start_snakes_json]

        response = app.post_json('/start', json_dict, status='*')
        self.assertEqual(response.status, '200 OK')

        json_body = json.loads(response.body)
        self.assertEqual(json_body, {
            u'taunt': u'battlesnake-python!',
        })

        private_state = main.db.hgetall(u'test-game')
        self.assertEqual(private_state, {
            'phase': 'hide',
        })

    def test_move_failure(self):
        app = TestApp(main.application)
        json_dict = start_game_json.copy()
        json_dict[u'snakes'] = [d.copy() for d in start_snakes_json]

        response = app.post_json('/move', json_dict, status='*')
        self.assertEqual(response.status, '404 Not Found')
