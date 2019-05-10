function GameManager(size) {
  this.size           = size; // Size of the grid
  this.inputManager   = new KeyboardInputManager;
  // this.actuator       = new Actuator;  // do I need this?

  this.actuator = new HTMLActuator;

  //creates a Grid
  this.grid = new Grid(this.size);

  // bind the move function to the inputManager
  this.inputManager.on("move", this.move.bind(this));
  this.inputManager.on("restart", this.restart.bind(this));
  // this.inputManager.on("keepPlaying", this.keepPlaying.bind(this));

  // initialize a new board with "gameID"
  console.log("start a new game" + this.grid.cells)
  this.setup();
  console.log(this.grid.cells)
}


// Initialize a new game and ask for a new "gameId"
GameManager.prototype.setup = function(){

  // get the gameId and the initial map
  var request = new XMLHttpRequest();
  request.open("GET", "/api/new_game");
  request.responseType = 'json';
  request.onload = () => {
    // gameId and highScore
    this.gameId = request.response['uId'];
    this.highScore = request.response['c_score'];

    // initialize the map
    updatedCells = request.response['board'];
    // fill the grid with new values
    for(var i = 0; i < updatedCells.length; i++) {
      for(var j = 0; j < updatedCells.length; j++) {
        var tile = updatedCells[i][j]

        // either create a new tile or set to null
        var position = ({ x : j, y : i});
        // update the grid position
        this.grid.cells[i][j] = (tile ? new Tile(position, tile) : null);
      }
    }
    // "print" the tiles to the grid
    this.actuator.actuate(this.grid, this.highScore)
      }
  request.send();
};


// Restart the game and asks for a new board and gameID
GameManager.prototype.restart = function(){
  this.actuator.continueGame(); // Clear the game won/lost message
  console.log("restart function")
  this.setup();
};


// get the fresh updated board from the backend
GameManager.prototype.move = function (direction) {
  // to "chanel" a global vairable into embedded function of XMLHttpRequest
  var self = this;

  // convert directon from '0123' to "wasd" format
  var moveType = "w";

  if (direction == 0){
    moveType = "w"
  }
  else if (direction == 1) {
    moveType = "d"
  }
  else if (direction == 2) {
    moveType = "s"
  }
  else if (direction == 3) {
    moveType = "a"
  }

  // console.log(direction)
  console.log(moveType)

  // Save current move with gameId
  var currentMove = JSON.stringify({"uId" : this.gameId, "direction" : moveType });

  // create object for request OR USE FETCH API https://scotch.io/tutorials/how-to-use-the-javascript-fetch-api-to-get-data
  var request = new XMLHttpRequest();

  // SEND "currentMove" to the server
  request.open("POST", "/api/play_the_game");
  request.setRequestHeader("Content-Type", "application/json");

  // RECIEVE the updated board due to "currentMove" fom the server
  request.onreadystatechange = function () {
    if (request.readyState === 4 && request.status === 200) {
      // console.log(this.grid.cells[0][1]);
      var json = JSON.parse(request.responseText);
      console.log(json);
      // get the new cells in 2D array
      var updatedCells = json['board'];
      // get the scores
      var metaData = json['c_score'];

      // // DEBUG
      // console.log("recieved 2D array is:  ");
      // console.log(updatedCells);
      // console.log("the actual score is :  ");
      // console.log(metaData);

      // fill the grid with new values
      for(var i = 0; i < updatedCells.length; i++) {
        for(var j = 0; j < updatedCells.length; j++) {
          var tile = updatedCells[i][j]
          // either create a new tile or set to null
          var position = ({ x : j, y : i});
          // update the grid position
          self.grid.cells[i][j] = (tile ? new Tile(position, tile) : null);
        }
      }
      // console.log("recieved 2D array converted to the grid:")
      // console.log(this.grid.cells)
      self.actuator.actuate(self.grid, metaData);
    }
  };
  console.log(this.grid);

  console.log(currentMove)
  request.send(currentMove);
};


// // Move tiles on the grid in the specified direction
// GameManager.prototype.move = function (direction) {
//   // 0: up, 1: right, 2: down, 3: left
//   var self = this;
//   console.log(direction)
//
//   // if (this.isGameTerminated()) return; // Don't do anything if the game's over
//
//   var cell, tile;
//
//   // var vector     = this.getVector(direction);
//   // var traversals = this.buildTraversals(vector);
//   var moved      = false;
//
//   // Save the current tile positions and remove merger information
//   // this.prepareTiles();
//
//   // Traverse the grid in the right direction and move tiles
//   traversals.x.forEach(function (x) {
//     traversals.y.forEach(function (y) {
//       cell = { x: x, y: y };
//       tile = self.grid.cellContent(cell);
//
//       if (tile) {
//         var positions = self.findFarthestPosition(cell, vector);
//         var next      = self.grid.cellContent(positions.next);
//
//         // Only one merger per row traversal?
//         if (next && next.value === tile.value && !next.mergedFrom) {
//           var merged = new Tile(positions.next, tile.value * 2);
//           merged.mergedFrom = [tile, next];
//
//           self.grid.insertTile(merged);
//           self.grid.removeTile(tile);
//
//           // Converge the two tiles' positions
//           tile.updatePosition(positions.next);
//
//           // Update the score
//           self.score += merged.value;
//
//           // The mighty 2048 tile
//           if (merged.value === 2048) self.won = true;
//         } else {
//           self.moveTile(tile, positions.farthest);
//         }
//
//         if (!self.positionsEqual(cell, tile)) {
//           moved = true; // The tile moved from its original cell!
//         }
//       }
//     });
//   });
//
//   if (moved) {
//     this.addRandomTile();
//
//     if (!this.movesAvailable()) {
//       this.over = true; // Game over!
//     }
//
//     this.actuate();
//   }
// };


// // // FOR TEST ING
// // create a GameManager
// var testGame = new GameManager();
//
//
// // console.log(test.getGrid());
// var updateGrid = testGame.move();



// console.log(GameManager);