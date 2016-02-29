package com.barefoot.bountysnake 
import PointJsonProtocol._

case class SnakeController(var gameState : Game){
  val snakeId = "1234-567890-123456-7890"
  var currentPosition : Point = Point(0,0)
  var path : List[Point] = List[Point]()
  var costGrid : Grid[Double] = Grid[Double](gameState.width,gameState.height)

  //update the state of the game from our model
  def updateState(gameState : Game){
    this.gameState = gameState

    //extract our position
    val ourSnake = gameState.snakes.filter(snake => snake.id == snakeId) 
    if(ourSnake.length != 1){
      //imposters or missing snakes
      println("Couldn't find our snake :( can't run a*"); //TODO: Throw exception
      return 
    }

    val headPosition = ourSnake.head.coords.headOption match {
      case Some(head) => {
        currentPosition = head

        //Create a new planner and board
        val enemies = gameState.snakes.filter(snake=>snake.id != snakeId)
        var planner : AStar = new AStar(costGrid)
        planner.buildGrid(enemies,gameState.food,gameState.walls,gameState.gold)

        //If there is food, go towards it
        if(!gameState.food.isEmpty){
          path = planner.planPath(head,gameState.food.head)
        } else {
          path = planner.planPath(head,Point(10,10))
        }
      }
      case None => println("Current position unkown. Can't run a*") //TODO: Throw exception
    }
  }

  def getNextMove() : String = {
    if(path.isEmpty){
      return "invalid" //TODO: throw expection
    }

    //just look at the path differences
    val deltaX = path.last.x - currentPosition.x
    val deltaY = path.last.y - currentPosition.y
    println(s"delta: $deltaX, $deltaY")
    if(deltaX==1){
      return "east"
    } else if (deltaX == -1){
      return "west"
    } else if (deltaY == 1){
      return "north"
    } else if(deltaY == -1){
      return "south"
    } else {
      return "invalid" //TODO: Throw exception
    }
  }
}
