import org.scalatest.FlatSpec
import net.liftweb.json._

class GameModelSpec extends FlatSpec {
    val json = """
    {
      "game": "hairy-cheese",
      "mode": "advanced",
      "turn": 0,
      "height": 20,
      "width": 30,
      "snakes": [
      {        
         "id": "1234-567890-123456-7890",
         "name": "Well Documented Snake",
         "status": "alive",
         "message": "Moved north",
         "taunt": "Let's rock!",
         "age": 56,
         "health": 83,
         "coords": [ { "x" : 1, "y" : 2} , { "x" : 2, "y" : 2} ],
         "kills": 4,
         "food": 12,
         "gold": 2
      }
      ],
      "food": [],
      "walls": [], 
      "gold": [] 
    }
    """


    "A Game" should "have valid properties" in {
      val game = JSONObjectFactory.createObject[Game](json) 
      assert(game.game == "hairy-cheese")
      assert(game.mode == "advanced")
      assert(game.turn == 0)
      assert(game.height == 20)
      assert(game.width == 30)
      assert(game.snakes.length == 1)
      assert(game.food.length == 0)
    }

    it should "allow adding valid points to the board" in {
      val game = JSONObjectFactory.createObject[Game](json)
      val board = Grid(game.width,game.height)
      game.snakes foreach { snake => board.addPoints(snake.coords,Enemy) }
      assert(board.values(1)(2) == Enemy)
      assert(board.values(2)(2) == Enemy)
    }

    it should "allow setting the entire grid to a certain value" in {
      val game = JSONObjectFactory.createObject[Game](json)
      val grid = Grid(game.width,game.height)
      grid.setGridToValue(Enemy)
      assert(grid.values(0)(0) == Enemy)
    }


}
