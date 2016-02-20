from bountysnakeai import a_star
from bountysnakeai import log

# Prefer lookups over a conditional
move_lut = [
    [u'invalid (0,0)', u'west', u'invalid (0,2)'],
    [u'north', u'invalid (1,1)', u'south'],
    [u'invalid (2,0)', u'east', u'invalid (2,2)']
]

def getSnake(board_state, snake_id):
    for snake in board_state.snake_list:
        if snake.id == snake_id:
            return snake
    return None

def health_threshold(board_state, snake):
    """
    Return the 'threshold' of health below which our snake should go find food.
    """
    # XXX: This is a very naive heuristic.
    path, cost = plan_path_to_food(board_state, snake)
    log.debug(path)
    log.debug(cost)

    return cost

def get_next_move_to_food(board_state, snake):
        '''
        Return the next best move to the food
        '''
        if len(board_state.food_list) < 1:
           return u"none"

        path, cost = plan_path_to_food(board_state, snake)
        if len(path) > 0:
                log.debug('Target move: %s,%s', path[1].x, path[1].y)

                # Turn path into a move we can pass back
                return compute_relative_move(path[1], snake_location)
        else:
                return u'none'

def plan_path_to_food(board_state, snake):
        if len(board_state.food_list) < 1:
           return ([], -1)

        # Create the grid for a*
        grid = a_star.build_grid(board_state.width, board_state.height, [], board_state.food_list)

        start_node = a_star.Node(snake.coords[0].x, snake.coords[0].y)

        # Plan a path to each of the food locations
        goals = [a_star.Node(goal.x, goal.y) for goal in board_state.food_list]
        paths_to_food = [
                a_star.find_path(grid, start_node, goal)
                for goals in goals
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
        return compute_relative_move(path[1], snake_location)

def path_to_optimal_corner(board_state, snake):
        '''
        Compares the paths to each of the corners, and picks the "best" one
        '''
        # 0. Set up  target locations
        head = snake.coords[0]
        start_location = a_star.Node(head.x, head.y)
        corners = [
            a_star.Node(0, 0), # top left
            a_star.Node(0, board_state.width-1), # top right
            a_star.Node(board_state.height-1, board_state.width-1), # bottom left
            a_star.Node(board_state.height-1, 0), # bottom right
        ]

        # 0b. Build grid
        grid = a_star.build_grid(board_state.width, board_state.height, [], [])

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
        start_location = a_star.Node(snake.coords[0].x, snake.coords[0].y)
        centre = a_star.Node(round(board_state.width), round(board_state.height))

        # Create the grid to plan on
        grid = a_star.build_grid(board_state.width, board_state.height, [], [])

        # Actually plan the path
        path_to_centre = a_star.find_path(grid, start_location, centre)

def get_next_move_to_centre(board_state, snake):
        '''
        Returns the next move to be taken to the centre of the board
        in a form that the game understands
        '''
        snake_location = snake.coords[0]
        path_to_centre = path_to_centre(board_state, snake)
        return compute_relative_move(path_to_centre[1], snake_location)

def compute_relative_move(move, snake_location):
        # Compute the difference (offset by one)
        delta_x = (move.x - snake_location[0]) + 1
        delta_y = (move.y - snake_location[1]) + 1
        return move_lut[delta_x][delta_y]

