import logging
import math
import random

from bountysnakeai import a_star
from bountysnakeai import model
from bountysnakeai import snakeID

log = logging.getLogger(__name__)

def getSnake(board_state, snake_id):
    for snake in board_state.snake_list:
        if snake.id == snake_id:
            return snake
    return None

def get_corners(board_state):
    return [
        a_star.Node(2, 2), # top left-ish
        a_star.Node(2, board_state.width-3), # top right-ish
        a_star.Node(board_state.height-3, board_state.width-3), # bottom left-ish
        a_star.Node(board_state.height-3, 2), # bottom right-ish
    ]

def should_hunt_for_food(board_state, snake):
    path, cost = plan_path_to_food(board_state, snake)
    log.debug('Have %s health; nearest food is %s away', snake.health, cost if cost != a_star.INFINITY else 'INF')
    if cost == a_star.INFINITY:
        # There is no reachable food :(
        return False
    elif (snake.health < 70) or (snake.health < cost*2):
        # If our snake is below 50% health, or food is far away, hunt!
        return True
    else:
        return False

def get_next_move_to_food(board_state, snake):
        '''
        Return the next best move to the food
        '''
        path, cost = plan_path_to_food(board_state, snake)
        if path:
            target = path[1].point
            log.debug('Target move: %s', target)

            # Turn path into a move we can pass back
            snake_location = snake.coords[0]
            return compute_relative_move(snake_location, target)
        else:
            raise Exception('needed a path to food and found none!')

def plan_path_to_food(board_state, snake):
        if not board_state.food_list:
           return ([], a_star.INFINITY)

        # Create the grid for a*
        grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list)

        start_node = a_star.Node.from_point(snake.coords[0])

        # Plan a path to each of the food locations
        goals = [a_star.Node.from_point(goal) for goal in board_state.food_list]
        paths_to_food = [
                a_star.find_path(grid, start_node, goal)
                for goal in goals
        ]

        path_costs = [
                path[-1].G if path else a_star.INFINITY
                for path in paths_to_food
        ]

        # Find the minimum cost path
        paths_plus_costs = zip(paths_to_food, path_costs)
        paths_plus_costs.sort(key=lambda t: t[1])
        return paths_plus_costs[0]

def is_too_risky_nearby(board_state, snake):
    # Construct a grid for our risk-averse snake
    grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list, risk_averse=True)
    head = snake.coords[0]

    # Determine if it's too risky
    node = grid[head.x][head.y]
    log.debug(' LOCAL RISKINESS: %.1f', node.riskiness)
    return (node.riskiness > 4.2)
#    return True

def get_to_safety(board_state, snake):
    safest_path = get_safest_path(board_state, snake)
    safest_direction = compute_relative_move(safest_path[0], safest_path[1])
    return safest_direction

def get_safest_path(board_state, snake):
    # Construct a grid for our risk-averse snake!
    grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list, risk_averse=True)

    # A node to represent our snake's head
    head = snake.coords[0]
    start_location = a_star.Node.from_point(head)

    # Pick 30 random locations on the board
    candidates = [
        grid[
            random.randint(0, board_state.width-1)
        ][
            random.randint(0, board_state.height-1)
        ]
        for _ in xrange(30)
    ]
    log.debug('GLOBAL RISKINESS: %s', ', '.join('%.1f'%c.riskiness for c in candidates if c.riskiness))

    # For each location, see which is the least risky to get to
    paths = [
        a_star.find_path(grid, start_location, candidate)
        for candidate in candidates
    ]
    # Filter out any that we just can't get, or that start and end in the
    # same place, and sort by cost (incorporates riskiness)
    tuples = [
        (path, path[1].G*4 + path[-1].G)
        for path in paths
        if len(path) > 1
    ]
    tuples.sort(key=lambda t: t[1])
    optimal_path, optimal_cost = tuples[0]

    if not tuples:
        # None of the 20 randomly selected points is reachable!
        log.debug('Could find no safe squares!')
        return []
    else:
        target_node = optimal_path[-1]
        log.debug('Picked the least risky path. Cost: %s. Heading to %s,%s', optimal_cost, target_node.x, target_node.y)
        return optimal_path

def get_next_move_to_corner(board_state, snake):
        '''
        Gets the next move to the corner, output in a useful format ('north','east', etc)
        '''
        snake_location = snake.coords[0]
        path = path_to_optimal_corner(board_state, snake)
        target = path[1].point
        return compute_relative_move(snake_location, target)

def path_to_optimal_corner(board_state, snake):
        '''
        Compares the paths to each of the corners, and picks the "best" one
        '''
        # 0. Set up  target locations
        head = snake.coords[0]
        start_location = a_star.Node.from_point(head)
        corners = get_corners(board_state)

        # 0b. Build grid
        grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list)

        # 1. Plan a path to each corner
        paths = [
            a_star.find_path(grid, start_location, corner)
            for corner in corners
        ]

        # 2. Compare the cost
        path_costs = [
            path[-1].G if path else a_star.INFINITY
            for path in paths
        ]
        triples = zip(corners, paths, path_costs)
        triples.sort(key=lambda t: t[2]) # sort by cost
        optimal_corner, optimal_path, optimal_cost = triples[0]

        if optimal_cost == a_star.INFINITY:
            # We couldn't find a good path :(
            # FIXME: maybe it's just that no corner was empty???
            log.debug('Could find no optimal corner')
            return []
        else:
            log.debug('Picked corner: %s,%s', optimal_corner.x, optimal_corner.y)
            return optimal_path

def compute_relative_move(snake_location, target):
    """
    For two contiguous squares, is the destination north, south, east, or west
    of the snake location?

    Remember that moving towards the x-axis is 'up'!
    """
    delta_x = target.x - snake_location.x
    delta_y = target.y - snake_location.y

    log.debug("Moving from %s to %s?", snake_location, target)

    # Ensure we're moving exactly one square north, south, east, or west
    assert abs(delta_x) + abs(delta_y) == 1

    if delta_x == 1:
        direction = 'east'
    elif delta_x == -1:
        direction = 'west'
    elif delta_y == 1:
        direction = 'south'
    elif delta_y == -1:
        direction = 'north'

    log.debug("Moving %s from %s to %s", direction, snake_location, target)
    return direction

def compute_relative_point(snake_location, direction):
    if direction == 'north':
        return model.Point(snake_location.x, snake_location.y-1)
    elif direction == 'east':
        return model.Point(snake_location.x+1, snake_location.y)
    elif direction == 'south':
        return model.Point(snake_location.x, snake_location.y+1)
    elif direction == 'west':
        return model.Point(snake_location.x-1, snake_location.y)
    else:
        raise ValueError('Unrecognized direction')

def snake_at_corner(board_state, our_snake) :
    head = our_snake.coords[0]
    position = a_star.Node.from_point(head)

    corners = get_corners(board_state)

    for corner in corners:
        distance = a_star.manhattan(position, corner)
        if corner_threshold(distance, our_snake) :
            return True
    return False

def corner_threshold(cost, snake):
    #TODO: make this a function of snake length
    return cost < 5

def circle(board_state, our_snake, previous_move):
    # Consider just enough of our snake to make up one side of the smallest
    # square box that it can circle around.
    snake_length = len(our_snake.coords)
    for side_length in xrange(2, snake_length):
        box_size = side_length**2 - (side_length-2)**2
        if box_size > snake_length:
            break
    head_point = our_snake.coords[0]
    front_points = our_snake.coords[:side_length]

    grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list)

    next_clockwise = {
        'north': 'east',
        'east': 'south',
        'south': 'west',
        'west': 'north',
        'None': 'west', # if there is no previous move, try to head west
    }
    next_counterclockwise = {
        'north': 'west',
        'west': 'south',
        'south': 'east',
        'east': 'north',
        'None': 'west', # if there is no previous move, try to head west
    }

    log.debug('Previous move: %s', previous_move)
    log.debug('front_points=%s', front_points)
    if (previous_move in ['north', 'south'] and not all(point.x == head_point.x for point in front_points)) \
    or (previous_move in ['east', 'west']   and not all(point.y == head_point.y for point in front_points)):
        # If the first side length of the snake isn't all going in the same
        # direction then continue, if possible, in the previous direction
        preferred_direction = previous_move
        log.debug('Haven\'t moved a side length yet. Stay the course %s.', preferred_direction)
    else:
        # Otherwise, we'd like to turn clockwise.
        preferred_direction = next_clockwise[previous_move]
        log.debug('Moved one side length, trying to turn %s!', preferred_direction)

    path = []
    start_node = a_star.Node.from_point(head_point)

    for i in xrange(4):
        goal_point = compute_relative_point(head_point, preferred_direction)
        goal_node = a_star.Node.from_point(goal_point)
        path = a_star.find_path(grid, start_node, goal_node)

        if path:
            return compute_relative_move(path[0].point, path[1].point)
        else:
            # If we didn't find a path forward, try turning clockwise again...
            preferred_direction = next_counterclockwise[preferred_direction]
            log.debug('Nowhere to go, trying to turn %s!', preferred_direction)

    else:
        raise AssertionError('Failed to find a point to move to after turning clockwise four times!')

def taunt_opponent(snakes,fatality=False):
    '''
    Selects one of the other snakes on the board and taunts it
    '''
    taunts = [
        ' is about to get creamed by this snake',
        ' looks drunk',
        ' needs to try harder',
        ' is clearly built out of crayon code',
        ' needs a little help from his friends',
        ' needs less leaf fru-fru, and more performance',
        ', food is for weak snakes',
        ' is on hunger strike',
        ' is a dirty camper',
        ' has no courage',
        ' will be trounced',
        '\'s creator spends too much time on reddit',
        ', last chance to back out',
        ' doesn\'t know when to quit',
        ' has no sense of pride',
    ]

    fatal_taunts = [
        ' can\'t stop killing itself',
        ', the walls are not for eating',
        ', winners don\'t use drugs',
        ' bit the dust',
        ' died. AGAIN.',
        ' employs Kamikaze tactics',
        ' is 6 feet below',
        ' went to a better place',
        ' was de-snaked',
        ' is FINISHED!',
        ' is starting to smell funky',
        ' didn\'t even stand a chance',
        ', better luck next time!',
        ', is sleeping on the job',
        ', makes dying look easy',
        ', please don\'t cry',
        ', is reconsidering some life choices',
    ]

    #Get all snakes that aren't us
    enemy_snakes = filter(lambda snake : snake.id != snakeID, snakes)
    if len(enemy_snakes) < 1:
        return ""
    #Randomly pick one
    snake = enemy_snakes[random.randint(0,len(enemy_snakes)-1)]

    #Randomly pick an appropriate taunt
    if fatality:
        taunt = fatal_taunts[random.randint(0,len(fatal_taunts)-1)]
    else:
        taunt = taunts[random.randint(0,len(taunts)-1)]

    final_taunt_string = str(snake.name) + taunt 
    log.debug("Taunting: %s", final_taunt_string)
    return final_taunt_string

def get_snakes_that_just_died(snakes,previous_snakes):
    '''
    Returns any snakes that died in the last turn
    '''

    if len(snakes) < 1 or len(previous_snakes) < 1:
        return []

    if len(snakes) == len(previous_snakes):
        return []
    else:
        #Dead snake will just disappear from the snake list
        current_snakes = set(snakes)
        new_dead_snakes = [ snake for snake in previous_snakes if snake not in current_snakes] 

        for dead_snake in new_dead_snakes:
            log.debug("Found new dead snake: %s", dead_snake.name)

        return new_dead_snakes
