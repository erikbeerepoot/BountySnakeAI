"use strict";

class GameController {

    constructor(){
        document.getElementById("btn_start").addEventListener("click", this.handler_btn_start.bind(this))
        document.getElementById("btn_move").addEventListener("click", this.handler_btn_move.bind(this))
        document.getElementById("btn_reset").addEventListener("click", this.handler_btn_reset.bind(this))

        this.gameState =
        {
         "game" : "tasty-nutsacks",
          "width" : 20,
          "height" : 20,
          "snakes" : [],
          "gold" : [{"x" : 2, "y" : 2}],
          "walls" : [],
          "food" : [{"x" : 5, "y" : 10}],
          "turn" : 0,
          "mode" : "basic"
        };
    
    }

    handler_btn_start(){
    }

    handler_btn_move(){
        //invoke move 
        post('move',this.gameState).then(function(response) {
            console.log("Success!", response);
        }, function(error) {
            console.error("Failed!", error);
        });

        //request path
        get('path').then(function(response) {
            var path = JSON.parse(response)
            var gameboard = document.getElementById("game_board")

            var width = 30
            var height = 30
            for(var coord in path){
                var element = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                element.setAttribute('x',path[coord].x * width)
                element.setAttribute('y',path[coord].y * height)
                element.setAttribute('width',width)
                element.setAttribute('height',height)
                element.setAttribute('class','path')
                gameboard.appendChild(element)
            }

        }, function(error) {
            console.error("Failed!", error);
        });


    }

    handler_btn_reset(){
    }
}

function get(url) {
  // Return a new promise.
  return new Promise(function(resolve, reject) {
    // Do the usual XHR stuff
    var req = new XMLHttpRequest();
    req.open('GET', url);

    req.onload = function() {
      // This is called even on 404 etc
      // so check the status
      if (req.status == 200) {
        // Resolve the promise with the response text
        resolve(req.response);
      }
      else {
        // Otherwise reject with the status text
        // which will hopefully be a meaningful error
        reject(Error(req.statusText));
      }
    };

    // Handle network errors
    req.onerror = function() {
      reject(Error("Network Error"));
    };

    // Make the request
    req.send();
  });
}


function post(url,data) {
  // Return a new promise.
  return new Promise(function(resolve, reject) {
    // Do the usual XHR stuff
    var req = new XMLHttpRequest();
    req.open('POST', url,true);

    req.setRequestHeader("Content-Type","application/json");
    req.send(JSON.stringify(data))

    req.onload = function() {
      // This is called even on 404 etc
      // so check the status
      if (req.status == 200) {
        // Resolve the promise with the response text
        resolve(req.response);
      }
      else {
        // Otherwise reject with the status text
        // which will hopefully be a meaningful error
        console.log(req.responseText)
        reject(Error(req.statusText));
      }
    };

    // Handle network errors
    req.onerror = function() {
      reject(Error("Network Error"));
    };

    // Make the request
    req.send();
  });
}



