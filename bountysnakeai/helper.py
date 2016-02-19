from a_star import *

#Prefer lookups over a conditional
move_lut =[[u'invalid (0,0)',u'west',u'invalid (0,2)'],[u'north',u'invalid (1,1)', u'south'],[u'invalid (2,0)',u'east',u'invalid (2,2)']]

def getSnake(board_state, snake_id):
    for snake in board_state.snake_list:
        if snake.id == snake_id:
            return snake
    return None

def health_threshold(board_state):
    """
    Return the 'threshold' of health below which our snake should go find food.
    """
    # XXX: This is a very naive heuristic.
    return (board_state.width * board_state.height) // 4

def get_next_move_to_food(board_state,snake):
        '''
        Return the next best move to the food
        '''
        if len(board_state.food_list) < 1:
           return u"none"


        snake_location = snake.coords[0] 
        food_location = board_state.food_list[0]

        start_node = Node(snake_location[0],snake_location[1])
        goalNode = Node(food_location[0],food_location[1])

        #Create the grid
        grid = build_grid(board_state.width, board_state.height, [], board_state.food_list)

        # Plan our path 
        path = find_path(grid,start_node,goalNode)
        log.debug('Current location: %s,%s', start_node.x,start_node.y)
        log.debug('Food location: %s,%s', food_location[0], food_location[1])
        log.debug('Target move: %s,%s', path[1].x,path[1].y)
        
        #Turn path into a move we can pass back
        return compute_relative_move(path[1],snake_location) 

def get_next_move_to_corner(board_state,snake):
        '''
        Gets the next move to the corner, output in a useful format ('north','east', etc)
        '''
        path = path_to_optimal_corner(board_state,snake)
        return compute_relative_move(path[1], snake_location)

def path_to_optimal_corner(board_state,snake):
        '''
        Compares the paths to each of the corners, and picks the "best" one
        '''
        #0. Set up  target locations 
        startLocation = Node(snake.coords[0][0],snake.coords[0][1])
        top_left = Node(0,0)
        top_right = Node(0,board_state.width-1) 
        bottom_right = Node(board_state.height-1,board_state.width-1)
        bottom_left =  Node(board_state.height-1,0)
        corners = [top_left,top_right,bottom_right,bottom_left]

        #0b. Build grid
        grid = build_grid(board_state.width,board_state.height, [], [])

        #1. Plan a path to each corner
        path_to_tl = find_path(grid,startLocation,top_left)         
        path_to_tr = find_path(grid,startLocation,top_right)         
        path_to_br = find_path(grid,startLocation,bottom_right)         
        path_to_bl = find_path(grid,startLocation,bottom_left)         
        paths = [path_to_tl,path_to_tr,path_to_br,path_to_bl]

        #2. Compare the cost 
        costs = []
        costs.append(path_to_tl[-1].G if len(path_to_tl) > 0 else [] )
        costs.append(path_to_tr[-1].G if len(path_to_tr) > 0 else [] )
        costs.append(path_to_br[-1].G if len(path_to_br) > 0 else [] )
        costs.append(path_to_bl[-1].G if len(path_to_bl) > 0 else [] )
        if len(costs) > 0:
                index_of_lowest_cost_path = costs.index(min(costs))
        else: 
                return []
        
        picked_corner = corners[index_of_lowest_cost_path]
        log.debug('Picked corner: %s,%s', picked_corner.x,picked_corner.y)
        return paths[index_of_lowest_cost_path]

def path_to_centre(board_state,snake):
        '''
        Plans a path to the centre of the board
        '''

        #We're planning a path between our current location and the centre
        start_location = Node(snake.coords[0][0],snake.coords[0][1])
        centre = Node(round(board_state.width),round(board_state.height))

        #Create the grid to plan on 
        grid = build_grid(board_state.width,board_state.height, [], [])

        #Actually plan the path
        path_to_centre = find_path(grid,start_location, centre)

def get_next_move_to_centre(board_state,snake):
        '''
        Returns the next move to be taken to the centre of the board
        in a form that the game understands
        '''
        snake_location = snake.coords[0]
        path_to_centre = path_to_centre(board_state,snake)
        return compute_relative_move(path_to_centre[1],snake_location)

def compute_relative_move(move,snake_location):
        #Compute the difference (offset by one)
        delta_x = (move.x - snake_location[0]) + 1
        delta_y = (move.y - snake_location[1]) + 1
        return move_lut[delta_x][delta_y]

