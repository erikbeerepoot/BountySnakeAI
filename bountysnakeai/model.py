from collections import namedtuple

class BoardState(object):
    """
    {
        "game": "hairy-cheese",
        "mode": "advanced",
        "turn": 0,
        "height": 20,
        "width": 30,
        "snakes": [
            <Snake Object>, ...
        ],
        "food": []
    }
    """
    def __init__(self, json_dict):
        self.game = json_dict['game']
        self.mode = json_dict['mode']
        self.turn = json_dict['turn']
        self.width = json_dict['width']
        self.height = json_dict['height']
        self.snake_list = [Snake(snake_dict) for snake_dict in json_dict['snakes']]
        self.food_list = [Point(*f) for f in json_dict['food']]

class Snake(object):
    """
    {
        "id": "1234-567890-123456-7890",
        "name": "Well Documented Snake",
        "status": "alive",
        "message": "Moved north",
        "taunt": "Let's rock!",
        "age": 56,
        "health": 83,
        "coords": [ [1, 1], [1, 2], [2, 2] ],
        "kills": 4,
    }
    """
    def __init__(self, json_dict):
        self.id = json_dict['id']
        self.name = json_dict['name']
        self.status = json_dict['status']
        self.message = json_dict['message']
        self.taunt = json_dict['taunt']
        self.age = json_dict['age']
        self.health = json_dict['health']
        self.coords = [Point(*c) for c in json_dict['coords']]
        self.kills = json_dict['kills']
        #self.food = json_dict['food']
        #self.gold = json_dict['gold']

Point = namedtuple('Point', ['x', 'y'])


