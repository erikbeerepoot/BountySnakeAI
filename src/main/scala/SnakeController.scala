package com.barefoot.bountysnake 
import PointJsonProtocol._

case class SnakeController(var gameState : Game){
  var path : List[Point] = List[Point]()
  var costGrid : Grid[Double] = Grid[Double](gameState.width,gameState.height)


  def updateState(gameState : Game){
    this.gameState = gameState

    costGrid = Grid[Double](gameState.width,gameState.height)
    var planner : AStar = new AStar(costGrid)

    path = planner.planPath(Point(1,1),Point(8,8))
  }
    
}
