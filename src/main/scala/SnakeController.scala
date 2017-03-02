package com.barefoot.bountysnake 
import PointJsonProtocol._

case class SnakeController(var gameState : Game){
  //Technically fixed, but at request time so var
  var snakeId = ""

  //Variable state that we update at each time step
  var path : List[Point] = List.empty
  var snake : Option[Snake] = None
  
  //Keeps track of the costs of each square
  var costGrid : Grid[Double] = Grid[Double](gameState.width,gameState.height)

  //update the state of the game from our model
  def updateState(gameState : Game){
    this.gameState = gameState
    snakeId = gameState.you

    //extract our position
    val ourSnake = gameState.snakes.filter(localSnake => localSnake.id == snakeId) 
    if(ourSnake.length != 1){
      //imposters or missing snakes
      println("Couldn't find our snake :( can't run a*"); //TODO: Throw exception
      return 
    }
    snake = ourSnake.headOption
    
    planPath()
  }

def planPath(){
  if(snake.isDefined==false){
    println("Can't plan path, our snake is undefined!")
  }
  val head = snake.get.coords.head

  //Create a new planner and board
  val enemies = gameState.snakes.filter(localSnake=>localSnake.id != snakeId)
  var planner : AStar = new AStar(costGrid)

  //Update food cost by relating to health
  Food.cost = -10 - 2*(100 - Math.min(snake.get.health_points,100))

  planner.buildGrid(snake.head,enemies,gameState.food,List.empty,List.empty)
  planner.grid.printGrid()
 
  //If there is food, go towards it
  if(snake.get.health_points < 25 || snake.get.coords.length < 15){
    path = planner.planPath(head,gameState.food.head)
    if(!hasNextMove){      
      println("Couldnt plan path to food. Trying to tail")            
    } else {
      return
    }

    //if we can't find a path to food
    path = planner.planPath(head,snake.get.coords.last)
    if(!hasNextMove){
      println("Couldnt plan path to tail. Randomly path planning ")      
    } else {
      return
    }  
  } else {
    path = planner.planPath(head,snake.get.coords.last)
    if(!hasNextMove){
      println("Couldnt plan path to tail. Randomly path planning ")      
    } else {
      return
    }

    planToCorner(planner)
    if(!hasNextMove){
      println("Couldnt plan path to corner.")
    } else {
      return
    }

    val nbs = planner.neighboursForNode(Node(snake.get.coords.head,0))  
    if(nbs.isEmpty==false){
      planner.planPath(head,nbs.head)
    }

     if(!hasNextMove){
      println("well and truly fucked!")
    } else {
      return 
    }
    




  }     
}


var targetCorner = Point(3,3)

def planToCorner(planner : AStar){
  val corners = List(Point(3,3),Point(gameState.height-3,3),Point(3,gameState.width-3),Point(gameState.height-3,gameState.width-3))

  val distances = corners.map(corner => planner.manhattanDistance(snake.get.coords.head,corner))
  val index = distances.indexOf(distances.reduceLeft(_ max _))
  val furthestCorner = corners(index)

  path = planner.planPath(snake.get.coords.head,furthestCorner)
  if(!hasNextMove){
    println("Couldnt find path to corner either")
  }
}

 def hasNextMove() : Boolean = {
    if(path.isEmpty){
      println("Empty path")
      return false
    }

    val coords = snake.get.coords
    val deltaX = path.last.x - coords.head.x
    val deltaY = path.last.y - coords.head.y
     if(deltaX == 1 || deltaX == -1 || deltaY == 1 || deltaY == -1) {
      return true
    } else {
      return false
    }
 }

def getNextMove() : String = {
  if(path.isEmpty){
    println("Empty path")
    return "invalid" //TODO: throw expection
  }

  if(snake.isDefined == false){
    println("Snake undefined")
    return "invalid"
  }
  val coords = snake.get.coords

  //just look at the path differences
  val deltaX = path.last.x - coords.head.x
  val deltaY = path.last.y - coords.head.y
  println(s"delta: $deltaX, $deltaY")


  if(deltaX==1){
    return "right"
  } else if (deltaX == -1){
    return "left"
  } else if (deltaY == -1){
    return "up"
  } else if(deltaY == 1){
    return "down"
  } else {
    println("delta wrong")
    return "right" //better than dying
    //return "invalid" //TODO: Throw exception
  }
}
}
