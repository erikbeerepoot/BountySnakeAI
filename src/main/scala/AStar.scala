import scala.collection.mutable.PriorityQueue
import scala.math.Ordering.Implicits._

case class Node(val point : Point, val priority : Int) extends Ordered[Node] {
  def compare(node : Node) = this.priority.compareTo(node.priority)
}


class AStar(grid : Array[Array[Int]], start : Node){  
    var closedSet = PriorityQueue[(Int,Node)]()
    var openSet = PriorityQueue[(Int,Node)]((0,start))




} 
