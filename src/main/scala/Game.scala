package com.barefoot.bountysnake

import scala.collection.mutable.ListBuffer
import spray.json._
import DefaultJsonProtocol._
import SnakeJsonProtocol._
import PointJsonProtocol._

case class StartObject(val game_id: String, val width : Int, val height : Int){}

//Game class
case class Game(val you : String, val game_id: String, val width : Int, val height : Int, var snakes : List[Snake],var food : List[Point],var dead_snakes : List[Snake], val turn : Int = 0){
}

object StartJsonProtocol extends DefaultJsonProtocol { 
  implicit val startFormat = jsonFormat3(StartObject)
}

object GameJsonProtocol extends DefaultJsonProtocol {
  implicit val gameFormat = jsonFormat8(Game)
    //,"game","mode","width","height","snakes","food","gold","walls")
}

case class GameTuple(val game : Game, val snakeController : SnakeController){}

object GameController {
  var games : ListBuffer[GameTuple] = ListBuffer[GameTuple]()

  //Attempt to lookup a game by name
  def lookupGameById(id : String) : Option[GameTuple] = {    
    val filteredGames = games.toList.filter({gameAndMore => gameAndMore.game.game_id == id})
    if(filteredGames.isEmpty){
      return None
    }
    return Some(filteredGames.head)
  }

  def snakeControllerForGame(id : String) : Option[SnakeController] = {
    lookupGameById(id) match {
      case Some(game) => Some(game.snakeController)
      case None => None
    }
  }

  def createGame(start : StartObject){
    val game = Game(start.game_id,"",start.width,start.height,List.empty,List.empty,List.empty)
    val newGameAndMore = GameTuple(game,SnakeController(game))
    games.append(newGameAndMore)
    println(s"Created game ${game}")
  }

  def createGame(game : Game){
    val newGameAndMore = GameTuple(game,SnakeController(game))
    games.append(newGameAndMore)
    println(s"Created game ${newGameAndMore}")
  }

  def removeGameById(id : String){
    lookupGameById(id) match {
      case Some(game) => games -= game
      case None =>
    }
  }
}

