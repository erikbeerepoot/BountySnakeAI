import numpy

from bountysnakeai.boards import Point
from bountysnakeai.boards import int_array
from bountysnakeai.boards import max_int

def retraced_path(current_point, parents_grid, number_to_delta):
    # Follow from the path of parents back from current->start
    path = []
    path.append(current_point)
    c_x, c_y = current_point
    parent_value = parents_grid[c_x][c_y]
    # A parent value of 0 means this node has no parent.
    while parent_value > 0:
        parent_delta = number_to_delta[parent_value]
        c_x = c_x + parent_delta[0]
        c_y = c_y + parent_delta[1]
        current_point = Point(c_x, c_y)
        path.append(current_point)
        parent_value = parents_grid[c_x][c_y]
    # Reverse the list so it goes start->current
    path.reverse()
    return path

def a_star(board, start_point, goal_point):
    # CONSTANTS:
    INFINITY = max_int
    UP, RIGHT, DOWN, LEFT = 1, 2, 3, 4
    neighbour_deltas = (
        ( 1,  0), # up
        ( 0,  1), # right
        (-1,  0), # down
        ( 0, -1), # left
    )
    number_to_delta = dict(zip(
        (UP, RIGHT, DOWN, LEFT),
        neighbour_deltas,
    ))
    delta_to_number = dict(zip(
        neighbour_deltas,
        (UP, RIGHT, DOWN, LEFT),
    ))

    def estimated_move_cost(from_x, from_y, to_x, to_y):
        # TODO: implement some useful metric for estimating the cost for
        #       moving from 'from' to its neighbour 'to'
        return 1
    max_estimated_cost = 1024

    # LOCAL SCOPE FOR EFFICIENCY:
    board_width, board_height = board.width, board.height
    obstacle_grid = board.obstacle_grid
    snake_grid = board.snake_grid
    food_grid = board.food_grid
    snakes = board.snakes
    board_size = board.width, board.height

    # TWO-DIMENSIONAL ARRAYS TO HOLD STATE
    h_score_grid = int_array(board_width, board_height, INFINITY)
    g_score_grid = int_array(board_width, board_height, INFINITY)
    f_score_grid = int_array(board_width, board_height, INFINITY)
    parents_grid = int_array(board_width, board_height, 0)
    visited_grid = int_array(board_width, board_height, 0)
    # XXX: only nodes currently in the 'open' set will have non-infinity
    #      values in the f_score_grid

    # Add the starting point to the open set and note that it costs nothing to
    # get there.
    start_x, start_y = start_point.x, start_point.y
    h_score_grid[start_x][start_y] = 0
    g_score_grid[start_x][start_y] = 0
    f_score_grid[start_x][start_y] = 0

    # While there are still nodes that are reachable but haven't been visited...
    while True:
        # Find the node in the open set with the lowest f_score
        _current = numpy.argmin(f_score_grid)
        c_x = _current // board_width
        c_y = _current % board_width
        current_point = Point(c_x, c_y)

        # If this node isn't actually in the open set, we've run out of
        # nodes in the open set before we found a path to the goal :(
        if f_score_grid[c_x][c_y] == INFINITY:
            raise ValueError('No Path Found')

        # If we've reached the destination node, retrace the path we took
        # and return it.
        if current_point == goal_point:
            return retraced_path(current_point, parents_grid, number_to_delta)

        # This node has been visited. Mark it as such.
        f_score_grid[c_x][c_y] = INFINITY
        visited_grid[c_x][c_y] = 1

        # For all neighbour nodes of the current node...
        for d_x, d_y in neighbour_deltas:
            # Apply the delta to the current coordinates to find the
            # neighbouring coordinates.
            n_x, n_y = c_x + d_x, c_y + d_y

            # Skip this neighbour if it is outside the grid, occupied by an
            # obstacle, or already visited:
            if not (0 <= n_x < board_width) \
            or not (0 <= n_y < board_height) \
            or obstacle_grid[n_x][n_y] \
            or visited_grid[n_x][n_y]:
                continue

            if f_score_grid[n_x][n_y] < INFINITY:
                # We've previously found a path to this node.

                # Check if the path we've just followed is shorter and,
                # if it is, update the optimal g_score and optimal parent/path.
                new_g = g_score_grid[c_x][c_y] \
                      + estimated_move_cost(c_x, c_y, n_x, n_y)
                if g_score_grid[n_x][n_y] > new_g:
                    g_score_grid[n_x][n_y] = new_g
                    parents_grid[n_x][n_y] = delta_to_number[(-d_x, -d_y)]
                    # re-calculate cached f_score, keep node in the open set
                    f_score_grid[n_x][n_y] = g_score_grid[n_x][n_y] \
                                           + h_score_grid[n_x][n_y]
            else:
                # This is the first time we've found a path to this node.

                # Calculate and store the g_score (i.e. total cost of this path
                # so far)
                g_score_grid[n_x][n_y] = g_score_grid[c_x][c_y] \
                                       + estimated_move_cost(c_x, c_y, n_x, n_y)

                # Calculate and store the h_score (i.e. the estimated distance
                # from this neighbour node to the goal node; currently using
                # the manhattan distance as the estimate)
                h_score_grid[n_x][n_y] = abs(n_x - goal_point.x) \
                                       + abs(n_y - goal_point.y)

                # Store instructions for getting from this node to its parent
                # along this best known path.
                parents_grid[n_x][n_y] = delta_to_number[(-d_x, -d_y)]

                # Calculate and store f_score, thereby implicitly adding this
                # neighbour to the 'open set' of nodes to be visited.
                f_score_grid[n_x][n_y] = g_score_grid[n_x][n_y] \
                                       + h_score_grid[n_x][n_y]