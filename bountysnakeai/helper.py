
class Node(object):
    def __init__(self, value, point, parent=None, H=0, G=0):
        self.value = value
        self.point = point
        self.parent = parent
        self.H = H
        self.G = G

    def move_cost(self,other):
        return self.value

    def __eq__(self, other):
        # Define equivalence as occupying the same coordinates
        if isinstance(other, Node):
            return self.point == other.point
        else:
            return False

    def __repr__(self):
        return u'Node(%r, %r, parent=%r, H=%r, G=%r)' % (
            self.value,
            self.point,
            self.parent if self.parent is None else 'Node(...)',
            self.H,
            self.G,
        )

def build_grid(width, height, snakes):
    grid = [[0 for x in range(height)] for x in range(width)]

    for x in range(width):
        for y in range(height):
            grid[x][y] = Node(1, (x,y))

    for snake in snakes:
        for coord in snake.coords:
            grid[coord[0]][coord[1]] = Node('%', coord[0], coord[1])

    return grid

def neighbours(node, grid):
    """
    Return a list of neighbour nodes within the grid.

    Neighbour nodes are defined to be:
    a) inside the grid
    b) directly above, below, left, or right of the given node
    c) not occupied by a snake
    """
    # Check that this isn't a dimensionless grid
    width = len(grid)
    if width == 0: return []
    height = len(grid[0])
    if height == 0: return []

    x, y = node.point
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
        if node.value != '%'
    ]
    return neighbouring_nodes

def manhattan(point,point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])

# Grid of Nodes, goal coords, start coords
def a_star(grid, goal, start):
    openset = set() #nodes we are currently examining
    closedset = set() #nodes we have eliminated

    # Add the starting point to the open set
    openset.add(start)

    # f_score is the sum of g_score + h_score
    # HACK: In order to make our ordering deterministic, we want to sort first
    #       by f_score, then by x and y coordinates. This will bias our paths
    #       to prefer those that move toward the origin of the grid, even when
    #       another direction would be equivalent, but it makes testing easier.
    f_score = lambda node: (node.G + node.H, node.point[0], node.point[1])

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

    #Throw an exception if there is no path
    raise ValueError('No Path Found')
    #TODO:  no path found...


def getCorner():
    #TODO: For each corner, check surrounding area for snakes, pick best corner relative to position to pass to A*
    return

def getFood():
    #TODO Find best food location to pass to A*
    return

def hide(width, height, snakes, player): #player is our snake
    grid = build_grid(width, height, snakes)
    goal = getCorner()
    move = a_star(grid, goal, player['coords'][0])

def getFood(width, height, snakes, player, food):
    grid = build_grid(width, height, snakes)
    goal = getFood()
    move = a_star(grid, goal, player['coords'][0])

def circle(width, height, snakes, player):
    grid = build_grid(width, height, snakes)
    length = len(player['coords'])
    # our snake should be turning every length/4 squares
