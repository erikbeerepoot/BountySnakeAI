package com.barefoot.bountysnake

import scala.collection.mutable.{Queue,PriorityQueue}
import scala.collection.mutable.ListBuffer
import scala.math.Ordering.Implicits._
import util.control.Breaks._


//Node class is just a point with a priority 
case class Node(val point : Point, val priority : Double = 0) extends Ordered[Node] {
  //Implicit ordering is lexicographical, which is not good enough for our purposes
  def compare(node : Node) = node.priority.compareTo(this.priority)
}

object AStar {
     //Returns the Euclidian distance between two points
    def euclidianDistance(pointA : Point, pointB : Point) : Double = {
       return math.sqrt(math.abs(pointA.y - pointB.y)^2 + math.abs(pointA.x - pointB.x)^2)
    }
   
    //Returns the Manhattan distance between two points 
    def manhattanDistance(pointA : Point, pointB : Point) : Int = math.abs(pointA.x - pointB.x) + math.abs(pointA.y - pointB.y)

}

class AStar(var grid : Grid[Double]){
    var closedSet = PriorityQueue[Node]()
    var openSet = PriorityQueue[Node]()

    //Keep track of the set of snakes
    var ourSnake : List[Point] = List.empty
    var enemies : List[Snake] = List.empty
    var deadEnemies : List[Snake] = List.empty

    //Keep track of any cavities (cached for performance reasons)
    var cavityPoints = List[Point]()

    //Add obstacles, etc. to the grid (each in one list)
    def buildGrid(ourSnake : Snake, snakes : List[Snake], dead_snakes : List[Snake], food : List[Point], walls : List[Point], gold : List[Point]){
      //Save the location of all snakes on the board
      this.ourSnake = ourSnake.coords
      enemies = snakes
      deadEnemies = dead_snakes

      //Clear grid first (so we dont keep old snake paths around)
      grid.setGridToValue(0.0)
      
      //Now set up our board
      grid.addPoints(ourSnake.coords,Infinity.cost)      
      grid.addPoints(food,Food.cost)
      grid.addPoints(walls,Wall.cost)
      grid.addPoints(gold,Gold.cost)

      //Add enemies to the grid 
      snakes foreach { 
        snake => grid.addPoints(snake.coords,Enemy.cost)
      }

      //Also add dead enemies, as they are still obstacles
      deadEnemies foreach {
       snake => grid.addPoints(snake.coords,Enemy.cost) 
      }

//      println("==-=-=-=-=-=-=-=-=-=-==")
//      println("==-= Board state: -=-==")
//      println("==-=-=-=-=-=-=-=-=-=-==")
//      grid.printGrid(List.empty)
//      println("==-=-=-=-=-=-=-=-=-=-==")
    } 

    def planPathWithFailedMessage(start : Point, goal : Point, failedMessage : String) : List[Point] = { 
      val path = planPath(start,goal)
      if(path.isEmpty){
        println(s"Path planning failed. Message: $failedMessage")
      }
      return path
    }

    //Attempts to plan a path from the start -> goal
    def planPath(start : Point, goal : Point) : List[Point] = {
        //First,Search for convex sets inside of loops
        cavityPoints = cavitySearch()

        //Now do A*
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
//            println("==-=-=-=-=-=-=-=-==")
//            println("==-= G Score: -=-==")
//            println("==-=-=-=-=-=-=-=-==")
//            g_score.printGrid(ourSnake)
//            println("-=-=-=-=-=-=-=-=-=-")


            return reconstructPath(originGrid,start,goal)
          }

          //Add the current node to the list of evaluated nodes
          closedSet.enqueue(current)
          
          //for each neighbour of current
          neighboursForNode(current) foreach { neighbour =>
            if(!pointInQueue(neighbour,closedSet)){
              val tentativeScore = g_score(current.point) + grid(neighbour) + AStar.euclidianDistance(current.point,neighbour)
              
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

    //Estimate the cost to a point
    def estimateCost(start : Point, goal : Point) : Double = {
       return AStar.manhattanDistance(start,goal) 
    }
 
    //Simply return the {N,S,E,W} neighbours, but discard squares we shouldn't move to
    //These squares could be the locations of enemies, or walls, etc.
    def neighboursForNode(node : Node) : List[Point] = {
      val x = node.point.x
      val y = node.point.y

      //get neighbouring nodes (if they exist)
      var neighbours = unfilteredNeighboursForNode(node)
      
      //Filter out any nodes that are part of the snakes body      
      neighbours = neighbours.filter(neighbour => !ourSnake.contains(neighbour))      
      
      //Also avoid other snakes (live ones)
      enemies.foreach(enemy => {
        neighbours = neighbours.filter(neighbour => !enemy.coords.contains(neighbour))      
      })

      //Handle dead snakes separately
      deadEnemies.foreach(enemy => {
        neighbours = neighbours.filter(neighbour => !enemy.coords.contains(neighbour))      
      })

      //Search for convex sets inside of loops
      if(cavityPoints.nonEmpty) {
        neighbours.filterNot(n => cavityPoints.contains(n))
      }

      neighbours.toList
    }

  def cavitySearch(): List[Point] = {
    //Filter out nodes that are inside of a loop we make with our body
    var cavityPoints = List[Point]()

    val loops = detectLoops(ourSnake)


    loops.map(loop => {
      //Find squares between tail and consecutive nodes to see if we can find empty
      val head = loop.head
        breakable {
        loop.foreach(segment => {
          var xRange: scala.collection.immutable.Range = head.x to segment.x
          if (segment.x < head.x) {
            xRange = head.x to segment.x by -1
          }

          var yRange: scala.collection.immutable.Range = head.y to segment.y
          if (segment.y < head.y) {
            yRange = head.y to segment.y by -1
          }

          //Convert to ListBuffer to equalize length
          var x = xRange.to[ListBuffer]
          var y = yRange.to[ListBuffer]

          while (y.length < x.length) {
            y = y :+ y.last
          }

          while (x.length < y.length) {
            x = x :+ x.last
          }

          //path, as the bird flies, between the two points
          val points = for ((x, y) <- (x zip y)) yield new Point(x, y)

          //filter out points that are part of the snake's body
          val nonBodyPoints = points.filter(point => !ourSnake.contains(point))

          if (nonBodyPoints.nonEmpty) {
            /* Now, we do a greedy expansion from this point. The result should be
             just the inside of this loop */
            cavityPoints ++= greedyExpansion(nonBodyPoints.head)
            break
          }
        })
      }
    })
    return cavityPoints.distinct
  }

    //Do a greedy expansion, finding all neighbours not part of our body
    def greedyExpansion(fromPoint: Point): List[Point] = {
      var openSet = Queue[Point]()
      var closedSet = Queue[Point]()
      var cavity = ListBuffer[Point]()

      //Don't expand more than the total number of nodes on the grid (heuristic)
      val maxExpansionNumber = grid.width * grid.height

      var count = 0
      openSet.enqueue(fromPoint)
      while(openSet.nonEmpty) {
        //Get a point we haven't explored yet
        val point = openSet.dequeue()
        closedSet.enqueue(point)
        cavity += point

        //Find all neighbours
        val neighbours = neighboursForPoint(point)

        //Filter to neighbours not part of our body
        var freeNeighbours = neighbours.filterNot(neighbour => ourSnake.contains(neighbour))

        //And haven't already been covered
        freeNeighbours = freeNeighbours.filterNot(f => closedSet.contains(f))

        //The explore them
        freeNeighbours.foreach(openSet.enqueue(_))

        //If we've exceeded our search treshold, just bail. Something went wrong
        count += 1
        if(count > maxExpansionNumber){
          return cavity.toList.distinct
        }

      }
      cavity.toList.distinct
    }

    //Wrapper to return unfiltered neighbours
    def unfilteredNeighboursForNode(node : Node) : List[Point] = {
        neighboursForPoint(node.point)
    }

    //returns the 4 immediate neighbours of this point
    def neighboursForPoint(point : Point) : List[Point] = {
        val x = point.x
        val y = point.y 

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
        if(y+1 < grid.height){
          neighbours += Point(x,y+1)
        }
        neighbours.toList
    }

    //Attempts to detect loops that our snake makes with itself, or with the board edges
    def detectLoops(forBody : List[Point]) : List[List[Point]] = {

      //8 is the smallest length at which a snake can form a loop (with ourselves) that can kill us
      if(forBody .length < 8){
        return List.empty
      }

      //Consider segments along with their neighbours
      var cycles : ListBuffer[List[Point]] = ListBuffer.empty
      for(startIdx <- 0 to (forBody.length-3)){
        val endIdx = Math.min(startIdx+3,(forBody.length))

        //Two adjacent vertices in our snake, and the midpoint 
        val sublist = forBody.slice(startIdx,endIdx).toList
        if(sublist.isEmpty){
          return List.empty
        }

        //Get all neighbours of this midpoint
        var point = Point(0,0)
        if(sublist.length == 3){
          //grab the middle segment
          point = sublist(1)
        } else {
          //just get the end
          point = sublist.last
        }
        val neighbours = neighboursForPoint(point)

        //Get the neighbours that aren't adjent vertices of the snake body
        val otherNeighbours = neighbours diff sublist

        //If the other neighbours are part of the snake's body, there must be a cycle
        val commonElements = otherNeighbours.filter(n => forBody contains n)
        if(commonElements.nonEmpty){
          //Include the body elements from point of contact to the body element that we contacted
          val fromIdx = forBody.indexOf(commonElements.head)
          val toIdx = forBody.indexOf(point)
          val cycle = forBody.slice(fromIdx,toIdx+1).toList
          if(cycle.nonEmpty) {
            cycles += cycle
          }
        }
      }

      //filter out non-distinct cycles
      val distinctCycles = filterCycles(cycles.toList)
      return distinctCycles.filter(!_.isEmpty)
    }

    //We may have several distinct cycles, but if they are part of the same cycle
    //each of the smaller cycles we found will be a subset of the longest cycle
    def filterCycles(cycles : List[List[Point]]): List[List[Point]] = {
      //if, for the current cycle, there is an element in cycles that contains it, we discard it
      cycles.filter(cycle => {
          !(cycles.exists(e => {
              (e containsSlice cycle) && (e != cycle)
          }))
      })
    }
} 
