package com.barefoot.bountysnake

import net.liftweb.json._


object SolidSnake{
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
  }
}

object JSONObjectFactory {
  implicit val formats = DefaultFormats

  def createObject[T](json : String)(implicit m: Manifest[T]) : T = {
    return parse(json).extract[T]
  }
}

