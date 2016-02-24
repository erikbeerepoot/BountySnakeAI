sealed trait GridValue { def name : String; def cost : Int }
case object Self extends GridValue { val name = "self"; val cost = 100 }
case object Enemy extends GridValue { val name = "enemy"; val cost = 100 }
case object Food extends GridValue { val name = "food"; val cost = -10 }
case object Gold extends GridValue { val name = "gold"; val cost = -100}
case object Wall extends GridValue { val name = "wall"; val cost = 100 }
case object Path extends GridValue { val name = "path"; val cost = 0 }


case class Board(val width : Int,val height : Int) {
  val values : Array[Array[GridValue]] = Array.ofDim[GridValue](width,height)

  def printBoard() = {
    values foreach { row => row foreach print; println }
  }

  def addPoints(points : List[Point], value : GridValue)= {
    points foreach { point => values(point.x)(point.y) = value }
  }
}
