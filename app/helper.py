
class Node:
    def __init__(self,value,point):
        self.value = value
        self.point = point
        self.parent = None
        self.H = 0
        self.G = 0
    def move_cost(self,other):
        return self.value

def build_grid(width, height, snakes):
    grid = [[0 for x in range(height)] for x in range(width)]

    for x in range(width):
        for y in range(height):
            grid[x][y] = Node(1, (x,y))

    for snake in snakes:
        for coord in snake.coords:
            grid[coord[0]][coord[1]] = Node('%', coord[0], coord[1])

    return grid

def children(point,grid):
    x,y = point.point
    links = [grid[d[0]][d[1]] for d in [(x-1, y),(x,y - 1),(x,y + 1),(x+1,y)]]
    return [link for link in links if link.value != '%'] # return coordinate if not a snake wall, ie. '%'

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
    #TODO: For each corner, check surrounding area for snakes, pick best corner relative to position
    return

def getFood():
    #TODO similar to getCorner, find best food location
    return

def hide(width, height, snakes, head):
    grid = build_grid(width, height, snakes)
    goal = getCorner()
    move = a_star(grid, goal, head)

def getFood(grid, width, height, head, food):
    grid = build_grid(width, height, snakes)
    goal = getFood()
    move = a_star(grid, goal, head)

def circle(grid, width, height, snake):
    length = len(snake.coords)
    # our snake should be turning every length/4 squares
