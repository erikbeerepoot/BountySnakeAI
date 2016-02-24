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
