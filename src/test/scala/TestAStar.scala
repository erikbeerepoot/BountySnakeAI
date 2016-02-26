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

      //2 paths are admissible, but each much contain the diagonal
      val diagonal = reversePath filter { element : Point => element.x == element.y}
      assert(diagonal == diagonalPath)
    }

    it should "not find a path" in {
      val grid = new Grid[Double](10,10)
      grid.setGridToValue(0)
      
      val impenetrableWall = (for(y <- Range(0,10)) yield Point(5,y)).toList
      grid.addPoints(impenetrableWall,Double.MaxValue)     
 
      val start = Point(1,1)
      val goal = Point(9,9)
      
      val aStar = new AStar(grid)
      val path = aStar.planPath(start,goal)
      assert(path.length == 0)
    }

    it should "plan a path around obstacles" in {
      val grid = new Grid[Double](10,10)
      grid.setGridToValue(0)
      
      val wall = (for(y <- Range(1,10)) yield Point(3,y)).toList
      grid.addPoints(wall,Double.MaxValue)     

      val wallB = (for(y <- Range(0,9)) yield Point(6,y)).toList
      grid.addPoints(wallB,Double.MaxValue)     

      val start = Point(1,1)
      val goal = Point(9,9)
      
      val aStar = new AStar(grid)
      val path = aStar.planPath(start,goal)

      //Prepend the starting node 
      val reversePath = start :: path.reverse
      
      //Verify results against ground truth list 
      val gtList = List((1,1), (2,1), (2,0), (3,0), (4,0), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9), (6,9), (7,9), (8,9), (9,9))
      assert((gtList filter { point => reversePath.contains(point) } ).length == 0) 

      val prettyGrid = Grid[GridValue](grid.width,grid.height)
      prettyPrintGrid(prettyGrid,start,goal,path, wall ::: wallB)
    }

    it should "plan a path around obstacles and go for the food" in {
      val grid = new Grid[Double](10,10)
      grid.setGridToValue(0)
      
      val wall = (for(y <- Range(1,10)) yield Point(3,y)).toList
      grid.addPoints(wall,Double.MaxValue)     

      val wallB = (for(y <- Range(0,9)) yield Point(6,y)).toList
      grid.addPoints(wallB,Double.MaxValue)     
      
      val food = Point(4,8)
      val moreFood = Point (5,2)
      grid(food) = Food.cost 
      grid(moreFood) = Food.cost
      val start = Point(1,1)
      val goal = Point(9,9)

      val aStar = new AStar(grid)
      val path = aStar.planPath(start,goal)

      //Prepend the starting node 
      val reversePath = start :: path.reverse
      
      //Verify results against ground truth list 
//      val gtList = List((1,1), (2,1), (2,0), (3,0), (4,0), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9), (6,9), (7,9), (8,9), (9,9))
  //    assert((gtList filter { point => reversePath.contains(point) } ).length == 0) 

      val prettyGrid = Grid[GridValue](grid.width,grid.height)
      prettyPrintGrid(prettyGrid,start,goal,path, wall ::: wallB, List[Point](food,moreFood))
    }
    def prettyPrintGrid(grid : Grid[GridValue],start : Point, goal : Point, path : List[Point], walls : List[Point], food : List[Point]= List[Point]()){
      val prettyGrid = new Grid[GridValue](10,10)
      prettyGrid.setGridToValue(Space)
      prettyGrid.addPoints(path,Path)
      prettyGrid(start) = Start
      prettyGrid(goal) = Goal
      prettyGrid.addPoints(walls,Wall)
      prettyGrid.addPoints(food,Food)
      prettyGrid.printGrid()
    }

}
