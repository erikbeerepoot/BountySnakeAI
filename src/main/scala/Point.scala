package com.barefoot.bountysnake

import spray.json._
import DefaultJsonProtocol._

case class Point(x : Int,y : Int){
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
  implicit object PointJsonFormat extends RootJsonFormat[Point] {
    def write(point : Point) = JsObject(
      "x" -> JsNumber(point.x),
      "y" -> JsNumber(point.y)
    )

    def read(value : JsValue) = {
      value.asJsObject.getFields("x","y") match {
      case Seq(JsNumber(x),JsNumber(y)) =>
        Point(x.toInt,y.toInt)
      case _ => throw new DeserializationException("Point expected!")
      }
    }
  }
}
