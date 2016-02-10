import bottle

snakeID = '0b303c04-7182-47f8-b47a-5aa2d2a57d5a'
snakeName = 'Workday'

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
    data = bottle.request.json

    # TODO: Do things with data
    # if data.snake[OUR SNAKE].status is 'alive' ...


    return {
        'move': 'north',
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
200
'''
@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: End game with ID data.game

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080)
