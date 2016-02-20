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

def get_corners(board_state):
    return [
        a_star.Node(0, 0), # top left
        a_star.Node(0, board_state.width-1), # top right
        a_star.Node(board_state.height-1, board_state.width-1), # bottom left
        a_star.Node(board_state.height-1, 0), # bottom right
    ]

def should_hunt_for_food(board_state, snake):
    path, cost = plan_path_to_food(board_state, snake)
    log.debug(path)
    log.debug(cost)
    if cost == a_star.INFINITY:
        # there is no food!
        return False
    elif snake.health < cost:
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
                log.debug('Target move: %s,%s', path[1].x, path[1].y)

                # Turn path into a move we can pass back
                return compute_relative_move(path[1], snake_location)
        else:
            return u"none"

def plan_path_to_food(board_state, snake):
        if not board_state.food_list:
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
        corners = get_corners(board_state)

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

def snake_at_corner(board_state, our_snake) :
    head = our_snake.coords[0]
    position = a_star.Node(head[0], head[1])

    corners = get_corners(board_state)

    for corner in corners:
        distance = a_star.manhattan(position, corner)
        if corner_threshold(distance, our_snake) :
            return True
    return False

def corner_threshold(cost, snake):
    #TODO: make this a function of snake length
    return cost < 5

def circle(board_state, our_snake, move):

    quarter = len(our_snake.coords)//4

    grid = a_star.build_grid(board_state.width, board_state.height, [], board_state.food_list)

    #Check if quarters worth of snake is going in the same direction. If not, continue if allowed
    if (move == 'north' or move == 'south'):
        for coord in our_snake.coords[:quarter]:
            if (our_snake.coords[0][0] != coord[0] and move_allowed(move, grid, our_snake.coords[0])):
                #continue in same direction if allowed
                return move
    else:
        for coord in our_snake.coords[:quarter]:
            if (our_snake.coords[0][1] != coord[1] and move_allowed(move, grid, our_snake.coords[0])):
                #continue in same direction if allowed
                return move

    #3rd. We need to turn. Choose direction that doesn't suck
    return choose_move(move, our_snake.coords[0][0], grid)

def move_allowed(direction, grid, head):
    try :
        if (direction == 'north'):
            return grid[head[0], head[1] - 1].contents != 1 #snake
        elif (direction == 'south'):
            return grid[head[0], head[1] + 1].contents != 1 #snake
        elif (direction == 'west'):
            return grid[head[0] - 1, head[1]].contents != 1 #snake
        else:
            return grid[head[0] + 1, head[1]].contents != 1 #snake
    except:
        # out of bounds, move would hit a wall
        return False

def choose_move(move, head, grid):
    #TODO: recover from one of these bad scenarios. Need to make our approach lend itself to a large enough clockwise circle
    if (move == 'north'):
        if (move_allowed('east', grid, head)):
            return 'east'
        return 'west' #can't circle. Hail mary to the only place we can go
    elif (move == 'east'):
        if (move_allowed('south', grid, head)):
            return 'south'
        return 'north' #can't circle. Hail mary to the only place we can go
    elif (move == 'south'):
        if (move_allowed('west', grid, head)):
            return 'west'
        return 'east' #can't circle. Hail mary to the only place we can go
    else:
        if (move_allowed('north', grid, head)) :
            return 'north'
        return 'south' #can't circle. Hail mary to the only place we can go
