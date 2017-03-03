package com.barefoot.bountysnake 
import PointJsonProtocol._

case class SnakeController(var gameState : Game){
    object SnakeState extends Enumeration {
      type SnakeState = Value
      val TargetFood, Squiggle, Dance = Value    
    }

    //Technically fixed, but at request time so var
    var snakeId = ""

    //Variable state that we update at each time step
    var path : List[Point] = List.empty
    var snake : Option[Snake] = None

    //Keeps track of the costs of each square
    var costGrid : Grid[Double] = Grid[Double](gameState.width,gameState.height)

    //update the state of the game from our model
    def updateState(gameState : Game){
      this.gameState = gameState
      snakeId = gameState.you

      //extract our position
      val ourSnake = gameState.snakes.filter(localSnake => localSnake.id == snakeId) 
      if(ourSnake.length != 1){
        //imposters or missing snakes
        println("Couldn't find our snake :( can't run a*"); //TODO: Throw exception
        return 
      }
      snake = ourSnake.headOption    
    }

    //Plan a path 
    def planPath(){
      if(snake.isDefined==false){
        println("Can't plan path, our snake is undefined!")
        return
      }
      val head = snake.get.coords.head

      //Create a new planner and board
      val enemies = gameState.snakes.filter(localSnake=>localSnake.id != snakeId)
      var planner : AStar = new AStar(costGrid)

      //Update food cost by relating to health
      Food.cost = - 5*(100 - Math.min(snake.get.health_points,100))

      //Build our cost grid (handy for viz. too!)
      planner.buildGrid(snake.head,enemies,gameState.dead_snakes,gameState.food,List.empty,List.empty)

      //Run state machine
      val state = determineState(planner)
      printCompleteState(state)

      state match {
        case SnakeState.TargetFood => {
          path = planner.planPath(head,gameState.food.head)
        }
        case SnakeState.Dance => {
          path = dance(planner)      
        }
        case SnakeState.Squiggle => {
          path = squiggle(planner)      
        }
      } 


      if(path.isEmpty){
        println("Unable to plan path using the normal methods. Attempting to follow our tail!")
        val tail = snake.get.coords.last
        val nbs = planner.neighboursForNode(Node(tail,0))

        path = planner.planPath(head,nbs.head)
      }

      if(path.isEmpty){
        println("Was unable to plan any path. Death is imminent!! Attempting last resort squiggle!")
        path = squiggle(planner)
      }
    }

    //Prints out all important state vars
    def printCompleteState(snakeState : SnakeState.SnakeState){
        println(s"Game: ${gameState.game_id}")
        println(s"Turn: ${gameState.turn}")
        println(s"State: $snakeState")
    }

    //Determine the current planning state
    def determineState(planner : AStar) : SnakeState.SnakeState = {
      if(!snake.isDefined){
        //Doesnt make sense, but returning something is better than nothing
        return SnakeState.Dance
      }

      val canKillOtherSnake = canKill(planner)
      println(s"canKill: $canKillOtherSnake")

      //If we're desperate for food, or we're not very long -> get food
      if(snake.get.health_points < (20 + Math.min(snake.get.coords.length,30)) || snake.get.coords.length < 25){
        return SnakeState.TargetFood
      } 

      //If food is close, also go and grab it
      if(AStar.manhattanDistance(snake.get.coords.head,gameState.food.head) < 4){
        return SnakeState.TargetFood
      }

      //Otherwise, just wag our tail
      return SnakeState.Dance
    }

    //Do a little squiggle if we can't get a* to plan anything further
    def squiggle(planner : AStar) : List[Point] = {
      val nbs = planner.neighboursForNode(Node(snake.get.coords.head,0))  
      if(nbs.isEmpty==false){
        return planner.planPath(snake.get.coords.head,nbs.head)
      }   
      return List.empty
    }

    //Can we starve the other snake by getting to the food first?
    def canKill(planner : AStar) : Boolean = {
      //If there are more than two snakes on the board, we can't single out a single snake
      if(gameState.snakes.length != 2){
        return false
      }

      //If there's more than 1 food on the board, this algorithm will be pointless
      if(gameState.food.length > 1){
        return false
      }

      //This is safe, since if two snakes -> 1 is an enemy, 1 is us
      val ourSnake = gameState.snakes.filter(localSnake => localSnake.id == snakeId).head
      val enemy = gameState.snakes.filterNot(localSnake => localSnake.id == snakeId).head

      //If they have more health than we have, we can't starve them
      if(enemy.health_points > ourSnake.health_points){
        return false
      }

      //If they're closer to the food, we can't beat 'em there
      //Since A* is optimal this should always work
      val theirPath = planner.planPath(enemy.coords.head,gameState.food.head)
      val ourPath = planner.planPath(ourSnake.coords.head,gameState.food.head)
      if(theirPath.length < ourPath.length){
        return false
      }

      return true
    }


    def pathAroundPoint(point : Point, planner : AStar) : List[Point] = {
      if(!snake.isDefined){
        return List.empty
      }

      if(snake.get.coords.length < 7 && ((snake.get.coords.length % 2) != 0)){
        return List.empty
      }

      //Make a rectangle with our body
      val height = 2
      val width = (snake.get.coords.length - 2) / 2

      val nbs = planner.neighboursForNode(Node(point,0))
      List.empty
    }

    //Do our little squiggly snake dance!
    def dance(planner : AStar) : List[Point] = {
      val corners = List(Point(3,3),Point(gameState.height-3,3),Point(3,gameState.width-3),Point(gameState.height-3,gameState.width-3))

      val distances = corners.map(corner => AStar.manhattanDistance(snake.get.coords.head,corner))
      val index = distances.indexOf(distances.reduceLeft(_ max _))
      val furthestCorner = corners(index)

      return planner.planPath(snake.get.coords.head,furthestCorner)  
    }

    //Can we dance? 
    def canDance(planner : AStar) : Boolean = {
      return !dance(planner).isEmpty
    }

    //Is there a valid next move?
    def hasNextMove() : Boolean = {
        if(path.isEmpty){
          println("Empty path")
          return false
        }

        val coords = snake.get.coords
        val deltaX = path.last.x - coords.head.x
        val deltaY = path.last.y - coords.head.y
         if(deltaX == 1 || deltaX == -1 || deltaY == 1 || deltaY == -1) {
          return true
        } else {
          return false
        }
    }

    //Get the next move in a form we can respond with
    def getNextMove() : String = {
      if(path.isEmpty){
        println("Empty path")
        return "invalid" //TODO: throw expection
      }

      if(snake.isDefined == false){
        println("Snake undefined")
        return "invalid"
      }
      val coords = snake.get.coords

      //just look at the path differences
      val deltaX = path.last.x - coords.head.x
      val deltaY = path.last.y - coords.head.y
      println(s"delta: $deltaX, $deltaY")

      //Turns our delta into a move we can respond with
      if(deltaX==1){
          return "right"
      } else if (deltaX == -1){
          return "left"
      } else if (deltaY == -1){
          return "up"
      } else if(deltaY == 1){
          return "down"
      } else {
          println("delta wrong")
          return "right" //better than dying    
      }
    }
}
