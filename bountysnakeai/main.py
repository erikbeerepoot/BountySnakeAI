import bottle
import os
import random
import redis

from bountysnakeai import helper
from bountysnakeai import model

snakeID = '0b303c04-7182-47f8-b47a-5aa2d2a57d5a'
taunts = [u"We're winning"]
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
db = redis.from_url(redis_url)

@bottle.route('/static/<path:path>')
def static(path):
    """
    Serve up static files.
    """
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    """
    Serve up some basic style information for our snakes.
    """
    head_url = u'%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        u'color': u'#3398CC',
        u'head': head_url
    }


@bottle.post('/start')
def start():
    """
    Initialize a new game.

    Return a taunt.
    """
    # Parse the game state out of the request body
    json_dict = bottle.request.json
    try:
        board_state = model.BoardState(json_dict)
    except KeyError, e :
        print("KeyError: We didn't get the dictionary we were excpecting")
        return {
            u'error' : u'You gave us invalid data! Missing key in json dict: ' + e.message 
        }



    # at game start, default to hide phase
    game_id = board_state.game
    private_state = {
        'phase': 'hide',
    }
    db.hmset(game_id, private_state)
    # TODO: Make sure unauthorized calls aren't overwriting an existing game state.

    # The game is about to start! Quick -- taunt the enemy!
    return {
        u'taunt': u'battlesnake-python!'
    }


@bottle.post('/move')
def move():
    """
    Process a 'move' on the game board.

    return a direction to move in and a taunt.
    """
    # Parse the game state out of the request body
    json_dict = bottle.request.json
 

    board_state = model.BoardState(json_dict)

    # Retrieve the stored game state
    game_id = board_state.game
    private_state = db.hgetall(game_id)

    # TODO: Make sure unauthorized calls aren't trying to predict our next move.

    if not private_state:
        # Someone has hit this endpoint before hitting /start,
        # or something else is wrong..
        bottle.abort(404, u"Game ID %s not found" % game_id)

    our_snake = helper.getSnake(board_state, snakeID)
    if not our_snake:
        bottle.abort(400, u"Bad Request: my snake is missing!")

    """
    TODO: implement something like this...

    if our_snake.health < helper.health_threshold(board_state):
        move = helper.getFood(board_state, our_snake)
    elif private_state['phase'] == 'circle':
        move = helper.circle(board_state, our_snake)
    else:
        move = helper.hide(board_state, our_snake)

    BUT: until we have that ...
    """
 
    if our_snake.health < helper.health_threshold(board_state,our_snake):
        #Compute our move relative to the current position 
        move = helper.get_next_move_to_food(board_state, our_snake)
    else:
        path_to_corner = helper.get_next_move_to_corner(board_state, our_snake)

        
    print("Move: " + move )

    return {
        u'move': move,
        u'taunt': random.choice(taunts)
    }



@bottle.post('/end')
def end():
    """
    End a game and clean up.

    Return a taunt.
    """
    # Parse the game state out of the request body
    json_dict = bottle.request.json
    board_state = model.BoardState(json_dict)

    # Delete the stored game state
    game_id = board_state.game
    db.delete(game_id)
    # TODO: Make sure unauthorized calls aren't trying to delete a game state.

    # The game is over -- any response will be ignored
    return {
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080) #TODO: change this to Heroku settings
