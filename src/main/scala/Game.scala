package com.barefoot.bountysnake

import scala.collection.mutable.ListBuffer
import spray.json._
import DefaultJsonProtocol._
import SnakeJsonProtocol._
import PointJsonProtocol._

//Game class
case class Game(val game: String, val mode : String, val width : Int, val height : Int, var snakes : List[Snake],var food : List[Point],var gold : List[Point],var walls : List[Point],val turn : Int = 0){
}

object GameJsonProtocol extends DefaultJsonProtocol {
  implicit val gameFormat = jsonFormat9(Game)
    //,"game","mode","width","height","snakes","food","gold","walls")
}

case class GameTuple(val game : Game, val snakeController : SnakeController){
}

object GameController {
  var games : ListBuffer[GameTuple] = ListBuffer[GameTuple]()

  //Attempt to lookup a game by name
  def lookupGameByName(name : String) : Option[GameTuple] = {
    val filteredGames = games.toList.filter({gameAndMore => gameAndMore.game.game == name})
    if(filteredGames.isEmpty){
      return None
    }
    return Some(filteredGames.head)
  }

  def snakeControllerForGame(name : String) : Option[SnakeController] = {
    lookupGameByName(name) match {
      case Some(game) => Some(game.snakeController)
      case None => None
    }
  }

  def createGame(game : Game){
    val newGameAndMore = GameTuple(game,SnakeController(game))
    games.append(newGameAndMore)
  }

  def removeGameByName(name : String){
    lookupGameByName(name) match {
      case Some(game) => games -= game
      case None =>
    }
  }
}

