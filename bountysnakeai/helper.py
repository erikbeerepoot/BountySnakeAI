from bountysnakeai.boards import Point
from bountysnakeai.boards import build_board
from bountysnakeai.pathfinding import a_star

def getCorner():
    #TODO: For each corner, check surrounding area for snakes, pick best corner relative to position to pass to A*
    return

def getFood():
    #TODO Find best food location to pass to A*
    return

def hide(width, height, snakes, player): #player is our snake
    board = build_board(width, height, snakes, [])
    goal_point = getCorner()
    start_x, start_y = player[u'coords'][0]
    start_point = Point(start_x, start_y)
    move = a_star(board, start_point, goal_point)

def getFood(width, height, snakes, player, food):
    board = build_board(width, height, snakes, food)
    goal_point = getFood()
    start_x, start_y = player[u'coords'][0]
    start_point = Point(start_x, start_y)
    move = a_star(board, start_point, goal_point)

def circle(width, height, snakes, player):
    board = build_board(width, height, snakes, food)
    length = len(player['coords'])
    # our snake should be turning every length/4 squares
