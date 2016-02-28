package com.barefoot.bountysnake

import scala.reflect.ClassTag
import spray.json._

case class Grid[A : ClassTag](val width : Int, val height : Int){
  var values : Array[Array[A]] = Array.ofDim[A](width,height)
 
  def apply(point : Point) = {
    values(point.x)(point.y)
  }

  def update(point : Point, value : A) = {
    values(point.x)(point.y) = value
  }

  def printGrid() = {
    values foreach { row => row foreach { value => value match {
      case value : GridValue => System.out.printf("%4s",value) 
      case point : Point => print(f"(${point.x},${point.y}),")  
      case number : Double => { 
        if(number == Double.MaxValue){
          printf("%5s","\u221e")
        } else {
          print(f"${number}%5.1f")
        }
      }
      case null =>  print("*****,")
    }
    }; println;
   }
  }


  def addPoints(points : List[Point], value : A) = {
    points foreach { point => values(point.x)(point.y) = value }
  }

  def setGridToValue(value : A){
    values = Array.tabulate(width,height)((x,y) => value)
  }
}


