package com.barefoot.bountysnake

import net.liftweb.json._
import spray.json._
import DefaultJsonProtocol._
import PointJsonProtocol._

case class Snake(val name : String,val id : String,var coords : List[Point], val taunt : String, val health_points : Int)

object SnakeJsonProtocol extends DefaultJsonProtocol {
  implicit val snakeFormat = jsonFormat5(Snake)
}

object SnakeFactory {
  implicit val formats = DefaultFormats

  def createSnakeFromJSON(json : String) : Snake = {
    return parse(json).extract[Snake]
  }
}


