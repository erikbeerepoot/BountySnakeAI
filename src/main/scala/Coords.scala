package com.barefoot.bountysnake

import spray.json._

case class Coords(coords : List[List[Int]]){}

object CoordsJsonProtocol extends DefaultJsonProtocol {
	implicit val pointFormat = jsonFormat1(Coords)  
}