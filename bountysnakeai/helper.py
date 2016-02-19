from a_star import *

#Prefer lookups over a conditional
moveLUT =[[u'invalid (0,0)',u'west',u'invalid (0,2)'],[u'north',u'invalid (1,1)', u'south'],[u'invalid (2,0)',u'east',u'invalid (2,2)']]

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

def compute_relative_move(move,snakeLocation):
        #Compute the difference (offset by one)
        delta_x = (move.x - snakeLocation[0]) + 1
        delta_y = (move.y - snakeLocation[1]) + 1
        print("del x: " + str(delta_x) + ", y: " + str(delta_y))
        return moveLUT[delta_x][delta_y]

