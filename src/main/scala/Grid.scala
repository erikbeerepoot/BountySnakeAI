sealed class GridValue(val cost : Int = 0, val name : String = "")
case object Self extends GridValue {override val name = "self"; override val cost = 100 }
case object Enemy extends GridValue {override val name = "enemy"; override val cost = 100 }
case object Food extends GridValue {override val name = "food"; override val cost = -10 }
case object Gold extends GridValue {override val name = "gold"; override val cost = -100}
case object Wall extends GridValue {override val name = "wall"; override val cost = 100 }
case object Path extends GridValue {override val name = "path"; override val cost = 0 }
case object Infinity extends GridValue {override val name = "infinity"; override val cost = Int.MaxValue}

case class Grid(val width : Int,val height : Int) {
  var values : Array[Array[GridValue]] = Array.ofDim[GridValue](width,height)

  def printBoard() = {
    values foreach { row => row foreach print; println }
  }

  def addPoints(points : List[Point], value : GridValue) = {
    points foreach { point => values(point.x)(point.y) = value }
  }

  def apply(node : Node) = values(node.point.x)(node.point.y)
  def apply(point : Point) = values(point.x)(point.y)

  def update(node : Node, value : Int) = values(node.point.x)(node.point.y) = new GridValue(value)
  def update(point: Point, value : Int) = values(point.x)(point.y) = new GridValue(value)

  def setGridToValue(value : GridValue) = {
    values = Array.tabulate(width,height)((x,y) => value)
  }
}
