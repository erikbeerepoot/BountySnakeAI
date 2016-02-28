package com.barefoot.bountysnake

import net.liftweb.json._
import spray.json._
import DefaultJsonProtocol._
import PointJsonProtocol._

case class Snake(val name : String,val id : String,val coords : List[Point],val status : String, val message : String, val taunt : String, val age : Int, val health : Int, val kills : Int, val food : Int, val gold : Int)

object SnakeJsonProtocol extends DefaultJsonProtocol {
  implicit val snakeFormat = jsonFormat11(Snake)
}

object SnakeFactory {
  implicit val formats = DefaultFormats

  def createSnakeFromJSON(json : String) : Snake = {
    return parse(json).extract[Snake]
  }
}

