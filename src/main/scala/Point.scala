package com.barefoot.bountysnake

import spray.json._

case class Point(val x : Int,val y : Int){
  def this(list : List[Int]) = {
    this(list(0),list(1))
  }

  override def toString(): String = {
    return "(" + x + "," + y + ")"
  }

  override def equals(o: Any) = o match {
    case p : Point => ((p.x == this.x) && (p.y == this.y))
    case _ => false
  }
}

object Point {
  def apply(list : List[Int]) = new Point(list)
}

object PointJsonProtocol extends DefaultJsonProtocol {
	//implicit val pointFormat = jsonFormat1(Point.apply)  
    implicit object PointJsonFormat extends RootJsonFormat[Point] {
	    def write(p : Point) = JsArray(JsNumber(p.x),JsNumber(p.y))

		def read(value : JsValue) = value match {
			case JsArray(Vector(JsNumber(x),JsNumber(y))) => {
				new Point(x.toInt,y.toInt)
			}
			case _ => deserializationError("Point expected")
		}
	}
}