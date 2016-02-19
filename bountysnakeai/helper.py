from a_star import *

#Prefer lookups over a conditional
moveLUT =[[u'invalid (0,0)',u'west',u'invalid (0,2)'],[u'south',u'invalid (1,1)', u'north'],[u'invalid (2,0)',u'east',u'invalid (2,2)']]

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

def get_food(board_state,snake):
        '''
        Return the next best move to the food
        '''
        if len(board_state.food_list) < 1:
           return u"none"


        snakeLocation = snake.coords[0] 
        foodLocation = board_state.food_list[0]

        startNode = Node(snakeLocation[0],snakeLocation[1])
        goalNode = Node(foodLocation[0],foodLocation[1])

        #Create the grid
        grid = build_grid(board_state.width, board_state.height, [], board_state.food_list)

        # Plan our path 
        path = find_path(grid,startNode,goalNode)
        print("Current location: " + str(startNode.x) + "," +  str(startNode.y))
        print("Food location: " + str(foodLocation[0]) + "," + str(foodLocation[1]))
        print("Target move: " + str(path[1].x) + "," + str(path[1].y))
        
        #Turn path into a move we can pass back
        return compute_relative_move(path[1],snakeLocation) 

def pick_corner(board_state,snake):
        '''
        Compares the paths to each of the corners, and picks the "best" one
        '''
        #0. Set up  target locations 
        startLocation = Node(snake.coords[0][0],snake.coords[0][1])
        top_left = Node(0,0)
        top_right = Node(0,board_state.width)
        bottom_right = Node(board_state.height,board_state.width)
        bottom_left =  Node(board_state.height,0)
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
                indexOfLowestCostPath = costs.index(min(costs))
        else: 
                return []
        
        #Debug
        picked_corner = corners[indexOfLowestCostPath]
        print("Picked corner: " + str(picked_corner.x) + "," + str(picked_corner.y))
        return costs[indexOfLowestCostPath]

def compute_relative_move(move,snakeLocation):
        #Compute the difference (offset by one)
        delta_x = (move.x - snakeLocation[0]) + 1
        delta_y = (move.y - snakeLocation[1]) + 1
        print("del x: " + str(delta_x) + ", y: " + str(delta_y))
        return moveLUT[delta_x][delta_y]

