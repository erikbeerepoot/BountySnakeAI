package com.barefoot.bountysnake 
import PointJsonProtocol._

case class SnakeController(var gameState : Game){
  var currentPoint : Point = Point(0,0)
  var path : List[Point] = List[Point]()
  var costGrid : Grid[Double] = Grid[Double](gameState.width,gameState.height)


  def updateState(gameState : Game){
    this.gameState = gameState

    costGrid = Grid[Double](gameState.width,gameState.height)
    var planner : AStar = new AStar(costGrid)

    path = planner.planPath(Point(1,1),Point(8,8))
  }

  def getNextMove() : String = {
    if(path.isEmpty){
      return "invalid" //TODO: throw expection
    }

    //just look at the path differences
    val deltaX = currentPosition.x - path.head.x
    val deltaY = currentPosition.x - path.head.y
    if(deltaX==1){
      return "east"
    } else if (deltaX==-1){
      return "west"
    } else if (deltaY==1){
      return "north"
    } else (deltaY==-1){
      return "south"
    } else {
      return "invalid" //TODO: Throw exception
    }

  }
    
}
