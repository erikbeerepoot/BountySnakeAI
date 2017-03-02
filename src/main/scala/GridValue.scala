package com.barefoot.bountysnake

import scala.reflect.ClassTag
import spray.json._


sealed class GridValue(var cost : Double = 0, val name : String = ""){
  override def toString() = "."
}
case object Self extends GridValue {override val name = "self"; cost = 200.0 }
case object Enemy extends GridValue {override val name = "enemy"; cost = Double.MaxValue }
case object Infinity extends GridValue {override val name = "infinity"; cost = Double.MaxValue}

case object Gold extends GridValue {
    override val name = "gold"
    cost = -100.0
    override def toString = "G"
}
case object Food extends GridValue {
    override val name = "food"
    cost = -10.0
    override def toString() = "\uD83C\uDF54"
}
case object Wall extends GridValue {
    override val name = "wall";
    cost = 100.0
    override def toString() = "="
}
case object Path extends GridValue {
    override val name = "path";
    cost = 0.0
    override def toString() = "P"
}
case object Space extends GridValue {
    override val name = "space"
    cost = 0.0
    override def toString() = "."
}
case object Start extends GridValue {
    override val name = "start"
    cost = 0.0
    override def toString() = "S"
}
case object Goal extends GridValue {
    override val name = "goal";
    cost = 0.0
    override def toString() = "G"
}

object GridValueJsonProtocol extends DefaultJsonProtocol {
  implicit object GridValueJsonFormat extends RootJsonFormat[GridValue] {
    def write(gridValue : GridValue) = JsObject(
      "name" -> JsString(gridValue.name),
      "cost" -> JsNumber(gridValue.cost)
    )

    def read(value : JsValue) = {
      value.asJsObject.getFields("name","cost") match {
        case Seq(JsString(name), JsNumber(cost)) => new GridValue(cost.toDouble,name)
        case _ => throw new DeserializationException("GridValue expected")
      }
    }
  }
}

