package com.barefoot.bountysnake

import scala.collection.mutable.ListBuffer
import scala.reflect.ClassTag
import spray.json._

case class Grid[A : ClassTag](val width : Int, val height : Int){
  var values : Array[Array[A]] = Array.ofDim[A](height,width)
 
  def apply(point : Point) = {
    values(point.x)(point.y)
  }

  def update(point : Point, value : A) = {
    values(point.x)(point.y) = value
  }

  def printGrid(snake : List[Point] = List.empty) = {
    for(y <- 0 to (height - 1)){
        for(x <- 0 to (width - 1)){
          val value = values(x)(y)
          value match { 
            case number : Double => printNumber(snake,x,y,number) 
            case point : Point => print(f"(${point.x},${point.y}),")  
            case null => print("_____,")
          }
        }; println;
    }
  }
 
  def printNumber(snake : List[Point],x : Int, y : Int, number : Double){
        //Print snake in grid
        if(snake.contains(Point(x,y))){                    
            if(Point(x,y) == snake.head){
               printf("%5s","\u25B2")
            } else {
              printf("%5s","\u25A0")
            }
        } else {
            if(number == Double.MaxValue){            
              printf("%5s","\u221e")            
            } else {
              print(f"${number}%5.1f")
            }          
        }
  }


  def addPoints(points : List[Point], value : A) = {
    points foreach { point => values(point.x)(point.y) = value }
  }

  def blurGrid(grid : Grid[Double]) : Grid[Double] = {
    for(x <- 0 to (width - 1)){
        for(y <- 0 to (height - 1)){
          val c = Point(x,y)
          val n = threeNeighbours(c)

          n.foreach(node => {
            grid.values(node.x)(node.y) = 0.25*grid.values(c.x)(c.y)                       
        })
      }
    } 
    return grid
  }

  def threeNeighbours(point : Point) : List[Point] = {
      val x = point.x
      val y = point.y 

      val minX = Math.max(0,x-3)
      val maxX = Math.min(width-1,x+3)
      val minY = Math.max(0,y-3)
      val maxY = Math.min(height-1,y+3)

      var square = ListBuffer[Point]()
      for(x <- minX to maxX){
        for(y <- minY to maxY){            
          square += Point(x,y)
        }
      }
      return square.toList
  }

  def setGridToValue(value : A){
    values = Array.tabulate(height,width)((x,y) => value)
  }
}


