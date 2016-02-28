package com.barefoot.bountysnake

import akka.actor.Actor
import spray.routing._
import spray.http._
import MediaTypes._
import spray.http.{ HttpHeaders, HttpOrigin, SomeOrigins }
import spray.routing.Directive0
import spray.routing.Directives._
import spray.httpx.SprayJsonSupport.sprayJsonMarshaller
import spray.httpx.SprayJsonSupport.sprayJsonUnmarshaller

// we don't implement our route structure directly in the service actor because
// we want to be able to test it independently, without having to spin up an actor
class MyServiceActor extends Actor with MyService {

  // the HttpService trait defines only one abstract member, which
  // connects the services environment to the enclosing actor or test
  def actorRefFactory = context

  // this actor only runs our route, but you could add
  // other things here, like request stream processing
  // or timeout handling
  def receive = runRoute(route)
}


// this trait defines our service behavior independently from the service actor
trait MyService extends HttpService {
  /** Directive providing CORS header support. This should be included in any application serving
    * a REST API that's queried cross-origin (from a different host than the one serving the API).
    * See http://www.w3.org/TR/cors/ for full specification.
    * @param allowedHostnames the set of hosts that are allowed to query the API. These should
    * not include the scheme or port; they're matched only against the hostname of the Origin
    * header.
    */
  def allowHosts(allowedHostnames: Set[String]): Directive0 = mapInnerRoute { innerRoute =>
    // Conditionally responds with "allowed" CORS headers, if the request origin's host is in the
    // allowed set, or if the request doesn't have an origin.
    println("allowHosts asdf asdf")
    optionalHeaderValueByType[HttpHeaders.Origin]() { originOption =>
      println(s"originOption: $originOption")
      // If Origin is set and the host is in our allowed set, add CORS headers and pass through.
      originOption flatMap {
        case HttpHeaders.Origin(list) => list.find {
          case HttpOrigin(_, HttpHeaders.Host(hostname, _)) => {
            println(s"origin: $list")
            allowedHostnames.contains(hostname)
          }
        }
      } map { goodOrigin =>
        respondWithHeaders(
          HttpHeaders.`Access-Control-Allow-Headers`(Seq("Origin", "X-Requested-With", "Content-Type", "Accept")),
          HttpHeaders.`Access-Control-Allow-Origin`(SomeOrigins(Seq(goodOrigin)))
        ) {
          options {
            complete {
              ""
            }
          } ~
          innerRoute
        }
        } getOrElse {
        // Else, pass through without headers.
        innerRoute
      }
    }
  }

  val route = {
    import GameJsonProtocol._
    //Most basic route to verify server is up
    path("") {
      get {
        allowHosts(Set[String]("http://127.0.0.1:8080")) {
          complete(StatusCodes.OK,"Complete")
        }
      }
    } ~
    //Endpoint used to get the game state for a given game
    pathPrefix("game" ){ 
      pathEnd {
        complete(StatusCodes.OK,s"Specify a game id using the next path component")
      } ~
      pathPrefix(Segment) { gameId => 
        val game = GameController.lookupGameByName(gameId)
        pathEnd {
          if(game.isEmpty){          
            complete(StatusCodes.OK,s"No game with name $gameId found")
          } else {
            complete(StatusCodes.OK,"Game found")
          }
        } ~ 
        path("state"){
          if(!game.isEmpty) {
            complete {
              game
            }
          } else {
            complete(StatusCodes.OK,s"No game with name $gameId found")
          }
        }
      } 
    } ~
    //Endpoint used to create a new game
    path("start") {
        post {
          entity(as[Game]) { game =>
            GameController.addGame(game)
            complete(StatusCodes.OK,s"Started game with name $game.game")
          }
        }
    } ~
    //Endpoint used to visualize games
    path("visualize"){
      getFromFile("/Users/erik/Dropbox/Projects/Programming/Scala/BountySnakeAI/visualization/html/board.html")
    } ~
    //Serve the JS as well
    pathPrefix("js"){
        print("serve js")
        getFromDirectory("/Users/erik/Dropbox/Projects/Programming/Scala/BountySnakeAI/visualization/js/")
    }
  }
}
