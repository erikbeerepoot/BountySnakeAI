import scala.reflect.ClassTag

sealed class GridValue(val cost : Double = 0, val name : String = ""){
  override def toString() = cost.toString
}
case object Self extends GridValue {override val name = "self"; override val cost = 100.0 }
case object Enemy extends GridValue {override val name = "enemy"; override val cost = 100.0 }
case object Food extends GridValue {override val name = "food"; override val cost = -10.0 }
case object Gold extends GridValue {override val name = "gold"; override val cost = -100.0}
case object Wall extends GridValue {override val name = "wall"; override val cost = 100.0 }
case object Infinity extends GridValue {override val name = "infinity"; override val cost = Double.MaxValue}

case object Path extends GridValue {
    override val name = "path"; 
    override val cost = 0.0
    override def toString() = "P"
}

case object Start extends GridValue { 
    override val name = "start" 
    override val cost = 0.0
    override def toString() = "S"
}

case object Goal extends GridValue { 
    override val name = "goal"; 
    override val cost = 0.0
    override def toString() = "G"
}

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
      case value : GridValue => System.out.printf("%4d",value) 
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


