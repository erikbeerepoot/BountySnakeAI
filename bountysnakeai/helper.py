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

def print_path(board, path):
    path = set(path)
    output = []
    line = ['+', '-'*(board.width*2+1), '+']
    output.append(''.join(line))
    for y in range(0, board.height):
        line = ['|']
        for x in range(0, board.width):
            if board.snake_grid[x][y] != -1:
                line.append(board.snake_grid[x][y])
            elif board.food_grid[x][y]:
                line.append('.')
            elif Point(x, y) in path:
                line.append('o')
            else:
                line.append(' ')
        line.append('|')
        output.append(' '.join(line))
    line = ['+', '-'*(board.width*2+1), '+']
    output.append(''.join(line))
    print '\n'.join(output)

def blah():
    for i in xrange(0, 1000):
        board = build_board(20, 20, [], [])
        path = a_star(board, Point(2,4), Point(18, 17))
        #print_path(board, path)

        path = a_star(board, Point(1,11), Point(11, 3))
        #print_path(board, path)

if __name__ == '__main__':
    from line_profiler import LineProfiler
    try:
        profiler = LineProfiler()
        profiler.add_function(blah)
        profiler.add_function(a_star)
        profiler.enable_by_count()
        blah()
    finally:
        profiler.print_stats()
