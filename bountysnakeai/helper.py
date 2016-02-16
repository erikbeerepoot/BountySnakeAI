
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

def children(node, grid):
    """
    Return a list of 'child' nodes within the grid.

    Child nodes are defined to be:
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
    child_nodes = [
        node for node in [
            grid[x_1][y_1] for x_1, y_1 in neighbouring_points
        ]
        # Filter out nodes that are occupied by a snake
        if node.value != '%'
    ]
    return child_nodes

def manhattan(point,point2):
    return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[0])

# Grid of Nodes, goal coords, start coords
def a_star(grid, goal, start):
    openset = set() #nodes we are currently examining
    closedset = set() #nodes we have eliminated
    #Current point is the starting point
    current = start
    #Add the starting point to the open set
    openset.add(current)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #If it is the item we want, retrace the path and return it
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]

        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children/siblings
        for node in children(current,grid):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score
                new_g = current.G + current.move_cost(node)
                if node.G > new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                node.H = manhattan(node, goal)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
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
