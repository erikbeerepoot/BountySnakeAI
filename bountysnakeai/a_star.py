EMPTY = 0
SNAKE = 1
FOOD = 2

INFINITY = 2**32 - 1 # For simplicity, just use a very high number...

class Node(object):
    def __init__(self, x, y, contents=EMPTY):
        # Coordinates of this node on the board.
        self.x = x
        self.y = y

        # Does this node contain part of a snake? food? nothing?
        self.contents = contents

        # The last node we visited on the path to this node.
        self.parent = None

        # g is the sum of the costs accrued on the path from the start node to
        # this node
        self.H = INFINITY

        # h is our guess as to how much it'll cost to reach the goal from this
        # node (if our graph is a grid, a naive approach would be to use the
        # manhattan distance as an estimate, for instance)
        self.G = INFINITY

    @property
    def F(self):
        return self.G + self.H

    def move_cost(self, neighbour):
        # Naively declare that it costs 1 to move from this node to any neighbour
        # TODO: come up with a better heuristic for the move cost
        return 1

    def __eq__(self, other):
        # Define equivalence as occupying the same coordinates
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __repr__(self):
        return u'Node(%r, %r)<cont=%r, H=%s, G=%s, parent=%s>' % (
            self.x,
            self.y,
            self.contents,
            'INF' if self.H >= INFINITY else self.H,
            'INF' if self.G >= INFINITY else self.G,
            '' if self.parent is None else 'Node(...)',
        )

def build_grid(width, height, snakes):
    grid = [
        [Node(x, y) for y in range(height)]
        for x in range(width)
    ]
    for snake in snakes:
        for p in snake.coords:
            node = grid[p.x][p.y]
            node.contents = SNAKE
    return grid

def neighbours(node, grid):
    """
    Return a list of available neighbour nodes within the game board.

    Available neighbour nodes are defined to be:
    a) inside the bounds of the board
    b) directly above, below, left, or right of the given node
    c) not occupied by a snake
    """
    # Check that this isn't a dimensionless grid
    width = len(grid)
    if width == 0: return []
    height = len(grid[0])
    if height == 0: return []

    x = node.x
    y = node.y
    neighbouring_points = [
        point
        for point in [
            # Left, below, above, right
            (x-1, y), (x, y-1), (x, y+1), (x+1, y)
        ]
        # Filter out points that are out of bounds
        if 0 <= point[0] < width
        and 0 <= point[1] < height
    ]
    neighbouring_nodes = [
        node for node in [
            grid[x_1][y_1] for x_1, y_1 in neighbouring_points
        ]
        # Filter out nodes that are occupied by a snake
        if node.contents != SNAKE
    ]
    return neighbouring_nodes

def manhattan(node_a, node_b):
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

def find_path(grid, goal, start):
    """
    Find the optimal path from the 'start' node to the 'goal' node within the
    provided grid of nodes.
    """
    openset = set() #nodes we are currently examining
    closedset = set() #nodes we have eliminated

    # Add the starting point to the open set
    openset.add(start)

    # HACK: In order to make our ordering deterministic, we want to sort first
    #       by f_score, then by x and y coordinates. This will bias our paths
    #       to prefer those that move toward the origin of the grid, even when
    #       another direction would be equivalent, but it makes testing easier.
    f_score = lambda node: (node.F, node.x, node.y)

    # While there are still nodes that are reachable but haven't been visited...
    while openset:
        # Find the node in the open set with the lowest f_score
        current = min(openset, key=f_score)

        # If we've reached the destination node, retrace the path we took
        # and return it.
        if current == goal:
            # Follow from the path of parents from goal->start
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            # Reverse the list so it goes start->goal
            return path[::-1]

        # This node has been visited. Mark it as such.
        openset.remove(current)
        closedset.add(current)

        # For all neighbour nodes of the current node...
        for node in neighbours(current, grid):

            if node in closedset:
                # If we've already visited this node, skip it
                continue

            elif node in openset:
                # If we've already found a path to this node, check if the
                # path we've just followed is shorter and, if it is, update the
                # optimal g_score and optimal parent/path.
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    node.G = new_g
                    node.parent = current
            else:
                # If this is the first time we've found a path to this node,
                # calculate the initial g_score and h_score, and update the
                # optimal g_score and optimal parent/path.
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                node.parent = current

                # Add this to the set of reachable nodes to visit in the future
                openset.add(node)
    else:
        raise ValueError('No Path Found')
