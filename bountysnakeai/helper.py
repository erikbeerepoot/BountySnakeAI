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
        
        grid = build_grid(board_state.width, board_state.height, [], board_state.food_list)
        path = find_path(grid,snake.coords[0],board_state.food_list[0])
        return path[0]

