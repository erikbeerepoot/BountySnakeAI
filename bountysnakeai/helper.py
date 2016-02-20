import math

from bountysnakeai import a_star
from bountysnakeai import model
from bountysnakeai import log

def getSnake(board_state, snake_id):
    for snake in board_state.snake_list:
        if snake.id == snake_id:
            return snake
    return None

def get_corners(board_state):
    return [
        a_star.Node(0, 0), # top left
        a_star.Node(0, board_state.width-1), # top right
        a_star.Node(board_state.height-1, board_state.width-1), # bottom left
        a_star.Node(board_state.height-1, 0), # bottom right
    ]

def should_hunt_for_food(board_state, snake):
    path, cost = plan_path_to_food(board_state, snake)
    log.debug('Have %s health; nearest food is %s away', snake.health, cost if cost != a_star.INFINITY else 'INF')
    if cost == a_star.INFINITY:
        # there is no food!
        return False
    elif snake.health < 80:
        # If our snake is going to die by the time it gets there, move to
        # the nearest food
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

def path_to_centre(board_state, snake):
        '''
        Plans a path to the centre of the board
        '''

        # We're planning a path between our current location and the centre
        start_location = a_star.Node.from_point(snake.coords[0])
        centre = a_star.Node(board_state.width//2, board_state.height//2)

        # Create the grid to plan on
        grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list)

        # Actually plan the path
        path_to_centre = a_star.find_path(grid, start_location, centre)

def get_next_move_to_centre(board_state, snake):
        '''
        Returns the next move to be taken to the centre of the board
        in a form that the game understands
        '''
        snake_location = snake.coords[0]
        path_to_centre = path_to_centre(board_state, snake)
        target = path_to_centre[1].point
        return compute_relative_move(snake_location, target)

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

    snake_length = len(our_snake.coords)
    # Round up to nearest multiple of 4
    snake_length = snake_length + ((4 - (snake_length % 4)) % 4)
    quarter = snake_length//4
    # Look at the head-quarter of the snake:
    head_point = our_snake.coords[0]
    front_points = our_snake.coords[:quarter]

    grid = a_star.build_grid(board_state.width, board_state.height, board_state.snake_list, board_state.food_list)

    next_clockwise = {
        'north': 'east',
        'east': 'south',
        'south': 'west',
        'west': 'north',
        'None': 'west', # if there is no previous move, try to head west
    }

    if (previous_move in ['north', 'south'] and not all(point.x == head_point.x for point in front_points)) \
    or (previous_move in ['east', 'west']   and not all(point.y == head_point.y for point in front_points)):
        # If the front quarter of the snake isn't all going in the same
        # direction then continue, if possible, in the previous direction
        preferred_direction = previous_move
    else:
        # Otherwise, we'd like to turn clockwise.
        preferred_direction = next_clockwise[previous_move]

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
            preferred_direction = next_clockwise[preferred_direction]

    else:
        raise AssertionError('Failed to find a point to move to after turning clockwise four times!')
