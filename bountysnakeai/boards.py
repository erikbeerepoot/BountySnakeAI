import numpy

from collections import namedtuple

Point = namedtuple(u'Point', [
    u'x',
    u'y',
])

Board = namedtuple(u'Board', [
    u'width',
    u'height',
    u'obstacle_grid',
    u'snake_grid',
    u'food_grid',
    u'snakes',
])

def int_array(width, height, default_value):
    # XXX: Return a two-dimensional array of signed 64-bit ints
    return numpy.full((width*height,), default_value, dtype=numpy.int64)

max_int = numpy.iinfo(numpy.int64).max

def build_board(width, height, snakes, food):
    obstacle_grid = int_array(width, height, 0)
    food_grid = int_array(width, height, 0)
    snake_grid = int_array(width, height, -1)

    for i, snake in enumerate(snakes):
        for x, y in snake[u'coords']:
            # Mark the id of the snake in position (x, y)
            snake_grid[x][y] = i
            obstacle_grid[x][y] = 1

    return Board(
        width = width,
        height = height,
        obstacle_grid = obstacle_grid,
        snake_grid = snake_grid,
        food_grid = food_grid,
        snakes = snakes,
    )

