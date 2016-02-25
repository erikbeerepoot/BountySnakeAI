import scala.collection.mutable.PriorityQueue
import scala.collection.mutable.ListBuffer
import scala.math.Ordering.Implicits._

case class Node(val point : Point, val priority : Int) extends Ordered[Node] {
  def compare(node : Node) = this.priority.compareTo(node.priority)
}


class AStar(var grid : Grid){

    var closedSet = PriorityQueue[Node]()
    var openSet = PriorityQueue[Node]()

    def buildGrid(snakes : List[Snake], food : List[Point], walls : List[Point], gold : List[Point]){
      snakes foreach { snake => grid.addPoints(snake.coords,Enemy)}
      grid.addPoints(food,Food)
      grid.addPoints(walls,Wall)
      grid.addPoints(gold,Gold)
    } 

    def planPath(start : Node, goal : Node){
        var closedSet = PriorityQueue[Node]()
        var openSet = PriorityQueue[Node](start)
        
        var originGrid = Grid(grid.width,grid.height)
        var g_score = Grid(grid.width,grid.height)
        var f_score = Grid(grid.width,grid.height)
        g_score.setGridToValue(Infinity)
        f_score.setGridToValue(Infinity)
        g_score(start) = 0
        f_score(start) = estimateCost(start,goal)

        while(!openSet.isEmpty){
          val current = openSet.dequeue()
          if(current == goal){
            return reconstructPath(originGrid,goal)
          }

          //Add the current node to the list of evaluated nodes
          closedSet.enqueue(current)
          
          //for each neighbour of current
          neighboursForNode(current) foreach { neighbour =>
            if(!pointInQueue(neighbour,closedSet)){
              val tentativeScore = g_score(current).cost + manhattanDistance(current.point,neighbour)
              
              //Discover a new node 
              if(!pointInQueue(neighbour,openSet) || tentativeScore <= g_score(neighbour).cost){
                originGrid(neighbour) = 1 
                g_score(neighbour) = tentativeScore
                f_score(neighbour) = g_score(neighbour).cost + estimateCost(neighbour,goal.point)
              } 
            }
          }
        }
        return List[Point]()
    }

    def reconstructPath(originGrid : Grid, goal : Node) : List[Point] = {
    }

    def pointInQueue(point : Point, queue : PriorityQueue[Node]) = {
      queue.find(element => element.point == point) match {
        case Some(node) => true
        case None => false 
      }
    }

    def estimateCost(start : Node, goal : Node) : Int = {
       manhattanDistance(start,goal) 
    }

    def estimateCost(start : Point, goal : Point) : Int = {
       manhattanDistance(start,goal) 
    }

    def manhattanDistance(nodeA : Node, nodeB : Node) : Int = math.abs(nodeA.point.x - nodeB.point.x) + math.abs(nodeA.point.y - nodeB.point.y)
    
    def manhattanDistance(pointA : Point, pointB : Point) : Int = math.abs(pointA.x - pointB.x) + math.abs(pointA.y - pointB.y)

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
