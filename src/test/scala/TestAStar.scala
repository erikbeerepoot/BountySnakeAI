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
    }

    it should "find the diagonal path" in {
      val grid = new Grid[Double](10,10)
      grid.setGridToValue(10)
      
      val diagonalPath = (for(x <- Range(1,10)) yield Point(x,x)).toList
      grid.addPoints(diagonalPath,0)     
 
      val start = Point(1,1)
      val goal = Point(9,9)
      
      val aStar = new AStar(grid)
      val path = aStar.planPath(start,goal)
      assert(path.length > 0)

      //Prepend the starting node 
      val reversePath = start :: path.reverse
      print(reversePath)

      //2 paths are admissible, but each much contain the diagonal
      val diagonal = reversePath filter { element : Point => element.x == element.y}
      assert(diagonal == diagonalPath)
    }

    it should "not find a path" in {
      val grid = new Grid[Double](10,10)
      grid.setGridToValue(0)
      
      val diagonalPath = (for(y <- Range(0,10)) yield Point(5,y)).toList
      grid.addPoints(diagonalPath,Double.MaxValue)     
 
      val start = Point(1,1)
      val goal = Point(9,9)
      
      val aStar = new AStar(grid)
      val path = aStar.planPath(start,goal)
      assert(path.length == 0)
    }


}
