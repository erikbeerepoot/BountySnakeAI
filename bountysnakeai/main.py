import bottle
import os
import random
import redis

from bountysnakeai import helper

snakeID = '0b303c04-7182-47f8-b47a-5aa2d2a57d5a'
taunts = ["We're winning"]
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
db = redis.from_url(redis_url)

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#3398CC',
        'head': head_url
    }

'''
REQUEST
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 0,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        , , ...
    ],
    "food": []
}

RESPONSE:
{
    "taunt": "Let's rock!"
}
'''

@bottle.post('/start')
def start():
    data = bottle.request.json

    db.hmset(data['game'], {'phase':'hide'}) #at game start, default to hide phase

    # TODO:
    # Initialize phase 1: hide

    return {
        'taunt': 'battlesnake-python!'
    }

'''
REQUEST
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        , , ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ]
}

RESPONSE:
{
   "move": "north",
   "taunt": "To the north pole!!"
}
'''
@bottle.post('/move')
def move():
    #TODO: data validation
    data = bottle.request.json
    gameData = db.hgetall(data['game'])
    if (not gameData):
        #TODO: Someone has hit this endpoint before hitting /start, or something else is wrong..
        return

    player = helper.getSnake(data['snakes'], snakeID)
    if (player is False):
        #TODO: error
        return {
            'move': 'north',
            'taunt': random.choice(taunts)
        }

    """
    TODO: implement something like this...

    if (player['health'] < helper.threshold(data['board'])):
        move = helper.getFood(data['board']['width'], data['board']['height'], data['snakes'], player, data['food'])
    elif (gameData['phase'] is 'circle'):
        move = helper.circle(data['board']['width'], data['board']['height'], data['snakes'], player)
    else:
        move = helper.hide(data['board']['width'], data['board']['height'], data['snakes'], player)

    BUT: until we have that ...
    """
    move = 'north'

    return {
        'move': move,
        'taunt': random.choice(taunts)
    }

'''
REQUEST
{
    "game": "hairy-cheese",
    "mode": "advanced",
    "turn": 4,
    "board": {
        "height": 20,
        "width": 30
    },
    "snakes": [
        , , ...
    ],
    "food": [
        [1, 2], [9, 3], ...
    ]
}

RESPONSE:
200
'''
@bottle.post('/end')
def end():
    data = bottle.request.json
    db.delete(data['game'])

    return {
        'taunt': 'Later!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080) #TODO: change this to Heroku settings
