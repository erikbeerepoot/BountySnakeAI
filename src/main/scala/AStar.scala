import scala.collection.mutable.PriorityQueue
import scala.collection.mutable.ListBuffer
import scala.math.Ordering.Implicits._

//Node class is just a point with a priority 
case class Node(val point : Point, val priority : Double = 0) extends Ordered[Node] {
  //Implicit ordering is lexicographical, which is not good enough for our purposes
  def compare(node : Node) = node.priority.compareTo(this.priority)
}

class AStar(var grid : Grid[Double]){

    var closedSet = PriorityQueue[Node]()
    var openSet = PriorityQueue[Node]()

    //Add obstacles, etc. to the grid (each in one list)
    def buildGrid(snakes : List[Snake], food : List[Point], walls : List[Point], gold : List[Point]){
      snakes foreach { snake => grid.addPoints(snake.coords,Enemy.cost)}
      grid.addPoints(food,Food.cost)
      grid.addPoints(walls,Wall.cost)
      grid.addPoints(gold,Gold.cost)
    } 

    //Attempts to plan a path from the start -> goal
    def planPath(start : Point, goal : Point) : List[Point] = {
        var closedSet = PriorityQueue[Node]()
        var openSet = PriorityQueue[Node](Node(start,0))
        
        var originGrid = Grid[Point](grid.width,grid.height)
        var g_score = Grid[Double](grid.width,grid.height)
        var f_score = Grid[Double](grid.width,grid.height)
        g_score.setGridToValue(Infinity.cost)
        f_score.setGridToValue(Infinity.cost)
        g_score(start) = 0 
        f_score(start) = estimateCost(start,goal)

        while(!openSet.isEmpty){
          val current = openSet.dequeue()
          if(current.point == goal){
            println(" ------------- g_score ----------------")
            g_score.printGrid()
            println(" --------------------------------------")
            
            println(" ------------- origin ----------------")
            originGrid.printGrid()
            println(" --------------------------------------")
           
            return reconstructPath(originGrid,start,goal)
          }

          //Add the current node to the list of evaluated nodes
          closedSet.enqueue(current)
          
          //for each neighbour of current
          neighboursForNode(current) foreach { neighbour =>
            if(!pointInQueue(neighbour,closedSet)){
              val tentativeScore = g_score(current.point) + grid(neighbour) + euclidianDistance(current.point,neighbour)
              
              //We've discovered a more efficient path 
              if(!pointInQueue(neighbour,openSet)){
                //discover a new node 
                val priority = tentativeScore + estimateCost(neighbour,goal)
                openSet.enqueue(Node(neighbour,priority))
              }
              if(tentativeScore < g_score(neighbour)){
                g_score(neighbour) = tentativeScore
                f_score(neighbour) = g_score(neighbour) + estimateCost(neighbour,goal)
                originGrid(neighbour) = current.point
              } 
            }
          }
        }
        return List[Point]()
    }

    //Reconstruct path traces the path back from the goal node to the origin to find the best path
    def reconstructPath(originGrid : Grid[Point] , start : Point, goal : Point) : List[Point] = {
      var path = ListBuffer[Point]()

      //Trace ancestors back from goal -> start
      var currentPoint = goal
      while(currentPoint != start){
        //If we encounter null at any point -> no path exists
        if(originGrid(currentPoint) == null){
          return List[Point]()
        }
        path += currentPoint
        currentPoint = originGrid(currentPoint)
      }
      return path.toList    
    }

    //Check if a node with this point is in the priority queue already
    def pointInQueue(point : Point, queue : PriorityQueue[Node]) = {
      queue.find(element => element.point == point) match {
        case Some(node) => true
        case None => false 
      }
    }

    def estimateCost(start : Point, goal : Point) : Double = {
       return manhattanDistance(start,goal) 
    }

    //Returns the Euclidian distance between two points
    def euclidianDistance(pointA : Point, pointB : Point) : Double = {
       return math.sqrt(math.abs(pointA.y - pointB.y)^2 + math.abs(pointA.x - pointB.x)^2)
    }
   
    //Returns the Manhattan distance between two points 
    def manhattanDistance(pointA : Point, pointB : Point) : Int = math.abs(pointA.x - pointB.x) + math.abs(pointA.y - pointB.y)

    //Simply return the {N,S,E,W} neighbours 
    def neighboursForNode(node : Node) : List[Point] = {
      val x = node.point.x
      val y = node.point.y

      //get neighbouring nodes (if they exist)
      var neighbours = ListBuffer[Point]()
      if(x>=1){
        neighbours += Point((x-1),y)
      }
      if(y>=1){
        neighbours += Point(x,y-1)
      }
      if(x+1<grid.width){
        neighbours += Point(x+1,y)
      }
      if(y+1<grid.height){
        neighbours += Point(x,y+1)
      }
      neighbours.toList
    }
} 
