import org.scalatest.FlatSpec
import net.liftweb.json._

class SnakeModelSpec extends FlatSpec {

  val snakeJSON = """ 
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
  """

  implicit val formats = DefaultFormats

  "A Snake" should "Get valid properties from JSON" in {
    
    val snake = JSONObjectFactory.createObject[Snake](snakeJSON)

    assert(snake.name == "Well Documented Snake")
    assert(snake.id == "1234-567890-123456-7890")
    assert(snake.status == "alive")
    assert(snake.message == "Moved north")
    assert(snake.taunt == "Let's rock!")
    assert(snake.age == 56)
    assert(snake.coords == List(Point(1,2),Point(2,2)))
    assert(snake.health == 83)
    assert(snake.kills == 4)
    assert(snake.food == 12)
    assert(snake.gold == 2)
  } 
}

