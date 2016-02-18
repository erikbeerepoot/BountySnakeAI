from bountysnakeai import a_star

def getSnake(snakes, snake_id):
    for snake in snakes:
        if (snake['id'] is snake_id):
            return snake
    return None

def threshold(board):
    return (board['width'] * board['height'] / 4) #threshold is a quarter of the area of the board. This may need to change depending on how much food is available

def getCorner():
    #TODO: For each corner, check surrounding area for snakes, pick best corner relative to position to pass to A*
    return

def getFood():
    #TODO Find best food location to pass to A*
    return

def hide(width, height, snakes, player): #player is our snake
    grid = build_grid(width, height, snakes)
    goal = getCorner()
    path = a_star.find_path(grid, goal, player['coords'][0])

def getFood(width, height, snakes, player, food):
    grid = build_grid(width, height, snakes)
    goal = getFood()
    path = a_star.find_path(grid, goal, player['coords'][0])

def circle(width, height, snakes, player):
    grid = build_grid(width, height, snakes)
    length = len(player['coords'])
    # our snake should be turning every length/4 squares
