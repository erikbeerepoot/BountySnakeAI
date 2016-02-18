from bountysnakeai import a_star

def getSnake(snakes, snake_id):
    for snake in snakes:
        if (snake['id'] is snake_id):
            return snake
    return None

def threshold(board):
    return (board['width'] * board['height'] / 4) #threshold is a quarter of the area of the board. This may need to change depending on how much food is available
