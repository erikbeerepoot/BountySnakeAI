package com.barefoot.bountysnake

import net.liftweb.json._

object JSONObjectFactory {
  implicit val formats = DefaultFormats

  def createObject[T](json : String)(implicit m: Manifest[T]) : T = {
    return parse(json).extract[T]
  }
}

