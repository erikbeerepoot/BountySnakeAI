import heapq
import logging

from bountysnakeai.model import Point

log = logging.getLogger(__name__)

EMPTY = 0
SNAKE = 1
FOOD = 2

INFINITY = 2**32 - 1 # For simplicity, just use a very high number...

class Node(object):
    __slots__ = [
        'x', 'y', 'contents', 'parent', 'H', 'G',
    ]
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
    def point(self):
        return Point(self.x, self.y)

    @classmethod
    def from_point(cls, point):
        return Node(point.x, point.y)

    def move_cost(self, neighbour):
        # Naively declare that it costs 1 to move from this node to any neighbour
        # TODO: come up with a better heuristic for the move cost
        return 1

    # XXX: Define equality comparisons as being based on the coordinates
    #      occupied by the Node. This makes it possible to do set membership
    #      tests without requiring both nodes be the same instance. e.g.
    #          Node(1, 1) in set([Node(1, 1)]) => True
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        else:
            return False
    # XXX: Define inequality comparisons as being based on the f score
    #      (where f = g +h) so that we can effeciently sort these nodes in a
    #      heap / priority queue.
    # XXX: In order to make our ordering deterministic, we want to sort first
    #      by f_score, then by x and y coordinates. This will bias our paths
    #      to prefer those that move toward the origin of the grid, even when
    #      another direction would be equivalent, but it makes testing easier.
    def __lt__(self, other):
        if isinstance(other, Node):
            return (self.G + self.H, self.x, self.y) \
                 < (other.G + other.H, other.x, other.y)
        else:
            return super(Node, self).__lt__(other)
    def __gt__(self, other):
        if isinstance(other, Node):
            return (self.G + self.H, self.x, self.y) \
                 > (other.G + other.H, other.x, other.y)
        else:
            return super(Node, self).__lt__(other)

    def __repr__(self):
        return u'Node(%r, %r)<cont=%r, H=%s, G=%s, parent=%s>' % (
            self.x,
            self.y,
            self.contents,
            'INF' if self.H >= INFINITY else self.H,
            'INF' if self.G >= INFINITY else self.G,
            '' if self.parent is None else 'Node(...)',
        )

def build_grid(width, height, snakes, food):
    grid = [
        [Node(x, y) for y in xrange(height)]
        for x in xrange(width)
    ]
    for snake in snakes:
        for p in snake.coords:
            node = grid[p.x][p.y]
            node.contents = SNAKE
    for p in food:
        node = grid[p.x][p.y]
        # If we're overwriting a snake there's a problem. Ensure valid state:
        assert node.contents == EMPTY
        node.contents = FOOD

    return grid

def neighbours(node, grid):
    """
    Return a list of available neighbour nodes within the game board.

    Available neighbour nodes are defined to be:
    a) inside the bounds of the board
    b) directly above, below, left, or right of the given node
    c) not occupied by a snake
    """
    # Assume that this isn't a dimensionless grid
    width = len(grid)
    height = len(grid[0])

    x = node.x
    y = node.y
    neighbouring_nodes = []

    # Filter out points that are out of bounds
    if x >= 1:
        neighbouring_nodes.append(grid[x-1][y])
    if y >= 1:
        neighbouring_nodes.append(grid[x][y-1])
    if x+1 < width:
        neighbouring_nodes.append(grid[x+1][y])
    if y+1 < height:
        neighbouring_nodes.append(grid[x][y+1])

    # Filter out nodes that are occupied by a snake
    return [
        neighbour
        for neighbour in neighbouring_nodes
        if neighbour.contents != SNAKE
    ]

def manhattan(node_a, node_b):
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

def find_path(grid, start, goal):
    """
    Find the optimal path from the 'start' node to the 'goal' node within the
    provided grid of nodes.
    """
    openset = set() #nodes we are currently examining
    closedset = set() #nodes we have eliminated

    # Set the starting node's costs
    start.G = 0
    start.H = manhattan(start, goal)

    # Add the starting point to the open set
    openset.add(start)
    openheap = [start]
    heappush, heappop = heapq.heappush, heapq.heappop

    # While there are still nodes that are reachable but haven't been visited...
    while openset:
        # Find the node in the open set with the lowest f_score
        # and mark it as visited.
        current = heappop(openheap)
        openset.remove(current)
        closedset.add(current)

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
                heappush(openheap, node)
    else:
        #Return an empty path
        log.debug('No path found, returning empty path list')
        return []

def print_grid(grid, start, goal, path=None):
    if not path: path = []

    width = len(grid[0])
    height = len(grid)
    output = []

    line = ['+', '-'*(width*4+1), '+']
    output.append(''.join(line))

    for y in range(0, height):
        line = ['|']
        for x in range(0, width):
            curr_node = Node(x, y)

            if curr_node == start:
                line.append('AAA')
            elif curr_node == goal:
                line.append('BBB')
            elif grid[x][y].contents == SNAKE:
                line.append(' S ')
            elif grid[x][y].contents == FOOD:
                line.append(' F ')
            elif curr_node in path:
                line.append('% 3s' % 'o')
            else:
                #line.append(' ')
                line.append('% 3s' % grid[x][y].G if grid[x][y].G != INFINITY else 'INF')

        line.append('|')
        output.append(' '.join(line))

    line = ['+', '-'*(width*4+1), '+']
    output.append(''.join(line))
    print '\n'.join(output)
