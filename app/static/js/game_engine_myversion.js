function GameManager(size) {
  this.size           = size; // Size of the grid
  this.inputManager   = new KeyboardInputManager;
  // this.actuator       = new Actuator;  // do I need this?

  this.actuator = new HTMLActuator;

  //creates a Grid
  this.grid = new Grid(this.size);

  // create metaData
  this.metaData = {
    c_score : 0,
    game_over : false,
    won : false
  };

  // bind the move and button functions to the inputManager
  this.inputManager.on("move", this.move.bind(this));
  this.inputManager.on("restart", this.restart.bind(this));  // restart button
  this.inputManager.on("keepPlaying", this.keepPlaying.bind(this)); // keepPlaying button
  this.inputManager.on("save", this.save.bind(this)); // Save button


  // initialize a new board with "gameID"
  console.log("start a new game with cells:")
  this.setup();
  console.log(this.grid.cells)
}


// Initialize a new game and ask for a new "gameId"
GameManager.prototype.setup = function(){
  var self = this;

  // get the gameId and the initial map
  var request = new XMLHttpRequest();
  request.open("GET", "/api/new_game");
  request.responseType = 'json';
  request.onload = () => {
    // gameId and highScore
    this.gameId = request.response['uId'];
    this.metaData.c_score = request.response['c_score'];

    // DEBUG
    // console.log("start game:")
    // console.log(this.metaData)

    // game canno be end at the first run
    // this.metaData.game_over = request.response['game_over'];

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
    this.actuator.actuate(this.grid, this.metaData)
    }
  request.send();
};


// Restart the game and asks for a new board and gameID
GameManager.prototype.restart = function(){
  this.metaData.game_over = false;
  this.metaData.won = false;

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
  // Save the current tile positions and remove merger information
  self.prepareTiles();
  console.log(self.grid.cells);

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

      var json = JSON.parse(request.responseText);
      // get the new cells in 2D array
      var updatedCells = json['board'];
      // console.log(self.metaData);
      self.metaData.c_score = request.response;
      self.metaData.c_score = json["c_score"];
      self.metaData.game_over = json["game_over"];
      var randomTile = json["newTile"];
      // console.log(randomTile[0]);

      // // DEBUG
      // console.log("recieved 2D array is:  ");
      console.log(updatedCells);

      // Save the current tile positions and remove merger information
      // self.prepareTiles();

      // console.log(self.grid.cells);
      var vector     = self.getVector(direction);
      // console.log(vector)
      var traversals = self.buildTraversals(vector);
      //
      console.log(vector);

      console.log("x: " + traversals.x);
      console.log("y: " + traversals.y);

      // traversals.x.forEach(function (x) {

      const randomX =  randomTile[1]
      const randomY =  randomTile[2]

      for(var i = 0; i < 4; i++) {

        // SLICE the old and updated Grid  to able to conpare it
        // line are always arranged into the moving direction
        var oldLine = [];
        var updatedLine = [];

        var mergeNr = 0;

        var oldCounter = 0;
        var newCounter = 0;

        for(var j = 0; j < 4; j++) {
          // horizontal move
          if (vector.y == 0){
            // move right
            if (vector.x == 1){
              oldLine.push(self.grid.cells[i][j])
              updatedLine.push(updatedCells[i][j])
            }
            // move left
            else if(vector.x == -1){
              oldLine.push(self.grid.cells[i][3 - j])
              updatedLine.push(updatedCells[i][3 - j])
            }
          }
          // vertical move
          else if (vector.x == 0){
            // move down
            if (vector.y == 1){
              oldLine.push(self.grid.cells[i][j])
              updatedLine.push(updatedCells[i][j])
            }
            // move up
            else if (vector.y == -1) {
              oldLine.push(self.grid.cells[i][j])
              updatedLine.push(updatedCells[i][j])
            }
          }

          // counts the non zero elements
          if(oldLine[j] != null){
            oldCounter += 1
          }else if (updatedLine[j] != 0){
            newCounter += 1
          }

        };//END OF line creating

        // DEBUG
        console.log("old line ")
        console.log(oldLine)
        console.log("newline is: " + updatedLine)
        console.log( "oldcounter: " + oldCounter, "newcounter :" + newCounter)

        // COUNT MERGES
        // nr is same
        if (oldCounter == newCounter){
          mergeNr = 0;
        // 1 merge happened in line
        }else if((oldCounter == 2 && newCounter == 1)
                ||(oldCounter == 3 && newCounter == 2)
                ||(oldCounter == 4 && newCounter == 3)){
          mergeNr = 1;
        // 2 merge happend in line
        }else if (oldCounter == 4 && newCounter == 2){
          mergeNr = 2;
        }

        console.log("nr of merge: " + mergeNr)

        // UPDATE COORDINATES
        // NO merge happend in the line
        if (mergeNr == 0){
          for(var k = 0; k < 4; k++) {
            var tile = null;
            // stayed at the same positon
            if (oldLine[k].value == updatedLine[k]){
              continue

            // element is moved so save it
            }else if (oldline[k].value != null && updatedLine[k] == 0){
              stack = oldline[k]
            }
            // push element from stack to new position
            if(stack.value == updatedLine[k]){
              tile.updatePosition()
            }
          }
        }else if (mergeNr = 1){

        }



          // Game is won
          if (updatedLine[k] == 2048){
            self.metaData.won = True;
          };

        };

      }

          // get the fresh value for
          var tile = updatedCells[i][j]

          // check if the game is won, HOW TO CHECK?
          if (tile == 2048){
            self.metaData.won = True;
          };

          // find out the new position
          // self.newPosition(self.direction, this.randomTile):

          // either create a new tile or set to null
          var position = ({ x : j, y : i});

          // // update the tile position
          // var merged = new Tile(position, tile);
          // // update Grid
          //
          // self.grid.insertTile(merged);
          // self.grid.removeTile(tile);


          // update the tile position
          self.grid.cells[i][j] = (tile ? new Tile(position, tile) : null);

      // console.log("recieved 2D array converted to the grid:")
      // console.log(this.grid.cells)
      self.actuator.actuate(self.grid, self.metaData);
    }
  };
  // console.log(this.grid);
  //
  // console.log(currentMove)
  request.send(currentMove);
};

// According to the current move ("0123"), slices a 1D array from the grid
// used to comapre incoming grid with current in JS
// GameManager.prototype.countMerge = function (oldline, updatedLine) {
//   const countMerge = 0;
//
//
//   if ((oldLine.length / arrSum2) == 1){
//     return 0;
//   }else if ((arrSum1 / arrSum2) == 2){
//
//   }
//
// };


// Keep playing after winning (allows going over 2048)
GameManager.prototype.keepPlaying = function () {
  this.actuator.continueGame(); // Clear the game won/lost message
  this.metaData.won = False;
};


// Save all tile positions and remove merger info
GameManager.prototype.prepareTiles = function () {
  this.grid.eachCell(function (x, y, tile) {
    if (tile) {
      tile.mergedFrom = null;
      tile.savePosition();
      // console.log(tile)
    }
  });
};


// Get the vector representing the chosen direction
GameManager.prototype.getVector = function (direction) {
  // Vectors representing tile movement
  var map = {
    0: { x: 0,  y: -1 }, // Up
    1: { x: 1,  y: 0 },  // Right
    2: { x: 0,  y: 1 },  // Down
    3: { x: -1, y: 0 }   // Left
  };

  return map[direction];
};


// Build a list of positions to traverse in the right order
GameManager.prototype.buildTraversals = function (vector) {
  var traversals = { x: [], y: [] };

  for (var pos = 0; pos < this.size; pos++) {
    traversals.x.push(pos);
    traversals.y.push(pos);
  }

  // Always traverse from the farthest cell in the chosen direction
  if (vector.x === -1) traversals.x = traversals.x.reverse();
  if (vector.y === -1) traversals.y = traversals.y.reverse();

  return traversals;
};


// Find where did the cell go
GameManager.prototype.findFarthestPosition = function (cell, vector) {
  var previous;

  // Progress towards the vector direction until an obstacle is found
  do {
    previous = cell;
    cell     = { x: previous.x + vector.x, y: previous.y + vector.y };
  } while (this.grid.withinBounds(cell) &&
           this.grid.cellAvailable(cell));

  return {
    farthest: previous,
    next: cell // Used to check if a merge is required
  };
};





// Save username and current score
GameManager.prototype.save = function () {
  // ask for usernam
  var name = prompt("Please enter your nickname!")

  // Save current move with gameId
  var userData = JSON.stringify({"c_score" : this.metaData.c_score, "u_name" : name });

  // create object for request OR USE FETCH API https://scotch.io/tutorials/how-to-use-the-javascript-fetch-api-to-get-data
  var request = new XMLHttpRequest();

  // SEND "currentMove" to the server
  request.open("POST", "/save_user_highscore");
  request.setRequestHeader("Content-Type", "application/json");

  request.send(userData);

  this.restart(); // Clear the game won/lost message
};
