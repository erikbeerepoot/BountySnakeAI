import bottle
import logging
import os
import random
import redis
import sys
import copy

from bountysnakeai import helper
from bountysnakeai import model
from bountysnakeai import log
from bountysnakeai import snakeID,turns_per_taunt

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
db = redis.from_url(redis_url)
previous_snakes = []

def log_json(fn):
    def wrapped(*args, **kwargs):
        result = fn(*args, **kwargs)
        log.debug('Response: %r', result)
        return result
    return wrapped

@bottle.route('/static/<path:path>')
@log_json
def static(path):
    """
    Serve up static files.
    """
    return bottle.static_file(path, root='static/')


@bottle.get('/')
@log_json
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
@log_json
def start():
    """
    Initialize a new game.

    Return a taunt.
    """
    # Parse the game state out of the request body
    json_dict = bottle.request.json
    log.debug(json_dict)

    try:
        board_state = model.BoardState(json_dict)
    except KeyError, e :
        print("KeyError: We didn't get the dictionary we were excpecting")
        return {
            u'error' : u'You gave us invalid data! Missing key in json dict: ' + e.message 
        }

    snakes_not_us = filter(lambda snake : snake.id != snakeID, board_state.snake_list)
    previous_snakes = copy.deepcopy(snakes_not_us)

    # at game start, default to hide phase
    game_id = board_state.game
    private_state = {
        'phase': 'hide',
        'move': None,
        'taunt': helper.taunt_opponent(snakes_not_us),
    }

    db.hmset(game_id, private_state)
    # TODO: Make sure unauthorized calls aren't overwriting an existing game state.

    log.info("BEGINNING GAME %s", game_id)

    # The game is about to start! Quick -- taunt the enemy!
    return {
        u'taunt': private_state['taunt']
    }


@bottle.post('/move')
@log_json
def move():
    """
    Process a 'move' on the game board.

    return a direction to move in and a taunt.
    """
    global previous_snakes

    # Parse the game state out of the request body
    json_dict = bottle.request.json
    log.debug(json_dict)
    log.info("MOVE CALLED")

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

    previous_phase = private_state['phase']
    previous_move = private_state['move']

    if helper.should_hunt_for_food(board_state, our_snake):
        # Any stage can lead to hunting if you get hungry enough.
        phase = 'food'
        move = helper.get_next_move_to_food(board_state, our_snake)
    elif helper.is_too_risky_nearby(board_state, our_snake):
        # Any stage can lead to Running, if it's risky enough nearby.
        phase = 'running'
        move = helper.get_to_safety(board_state, our_snake)
    elif (previous_phase == 'circle') or helper.snake_at_corner(board_state, our_snake):
        # Hiding should result in finding a corner, which leads to Circling.
        phase = 'circle'
        move = helper.circle(board_state, our_snake, previous_move)
    else:
        # Food and Running can lead to Hiding in a corner.
        if "hiding-in-" not in previous_phase:
            # Lets pick a place to hide
            phase = "hiding-in-corner" if random.randint(1,20)==5 else "hiding-in-centre"

        if "hiding-in-corner" in phase:
            move = helper.get_next_move_to_corner(board_state, our_snake)
        else:
            move = helper.get_next_move_to_centre(board_state, our_snake)

    log.info(' GAME: %s', game_id)
    log.info('PHASE: %s', phase)
    log.info(' MOVE: %s', move)

    #log.debug(previous_snakes)
    newly_dead_snakes = helper.get_snakes_that_just_died(board_state.snake_list, previous_snakes)
    if not newly_dead_snakes:
        # If there are no new dead snakes, taunt every so often
        if board_state.turn % turns_per_taunt == 0:
            alive_snakes = filter(lambda snake : snake.status == "alive", board_state.snake_list)
            taunt = helper.taunt_opponent(alive_snakes)
            private_state['taunt'] = taunt
        else:
            taunt = private_state['taunt']
    else:
        taunt = helper.taunt_opponent(newly_dead_snakes,fatality=True)
        private_state['taunt'] = taunt

    previous_snakes = copy.deepcopy(board_state.snake_list)
    private_state['move'] = move
    private_state['phase'] = phase
    db.hmset(game_id, private_state)

    return {
        u'move': move,
        u'taunt': taunt
    }



@bottle.post('/end')
@log_json
def end():
    """
    End a game and clean up.

    Return a taunt.
    """
    # Parse the game state out of the request body
    json_dict = bottle.request.json
    log.debug(json_dict)
    board_state = model.BoardState(json_dict)

    # Delete the stored game state
    game_id = board_state.game
    db.delete(game_id)
    # TODO: Make sure unauthorized calls aren't trying to delete a game state.

    log.info("ENDING GAME %s", game_id)

    # The game is over -- any response will be ignored
    return {
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host='127.0.0.1', port=8080) #TODO: change this to Heroku settings
