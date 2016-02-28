package com.barefoot.bountysnake

import spray.json._

case class Point(val x : Int,val y : Int){
  def this(list : List[Int]) = {
    this(list(0),list(1))
  }

  override def toString(): String = {
    return "(" + x + "," + y + ")"
  }
}

object Point {
  def apply(list : List[Int]) = new Point(list)
}


object PointJsonProtocol extends DefaultJsonProtocol {
  implicit val pointFormat = jsonFormat2(Point.apply)
}

