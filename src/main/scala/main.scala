import net.liftweb.json._


object SolidSnake{
  def main(args: Array[String]): Unit = {
    println("Hello, world!")
  }
}

class Game(val game: String, val mode : String, val width : Int, val height : Int, var snakes : List[Snake],var food : List[Point],var gold : List[Point],var walls : List[Point]){
  var turn : Int = 0

}

object JSONObjectFactory {
  implicit val formats = DefaultFormats

  def createObject[T](json : String)(implicit m: Manifest[T]) : T = {
    return parse(json).extract[T]
  }
}

