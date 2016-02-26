import org.scalatest.FlatSpec

class AStarSpec extends FlatSpec {

    "AStar " should "plan a basic path" in {
      val grid = new Grid[Double](10,10)
      grid.setGridToValue(0)
      
      val start = Point(1,1)
      val goal = Point(9,9)
      
      val aStar = new AStar(grid)
      val path = aStar.planPath(start,goal)
      assert(path.length > 0)
     
      print(path)
      path foreach { point => grid(point) = Path.cost }
      grid.printGrid()
    }
}
