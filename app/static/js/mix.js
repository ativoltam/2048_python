function GameManager(size) {
  this.size           = size; // Size of the grid
  this.inputManager   = new KeyboardInputManager;
  // this.actuator       = new Actuator;  // do I need this?

  this.actuator = new HTMLActuator;

  //creates a Grid
  // this.grid = new Grid(this.size);

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
  this.setup();
}


// Initialize a new game and ask for a new "gameId"
GameManager.prototype.setup = function(){
  var self = this;

  this.grid = new Grid(this.size);

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
    // DEBUG


  request.send();
  console.log("start a new game with cells:")
  console.log(self.grid.cells)
  console.log("setup is called")
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
  var moveType = null;

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
  // Save the current tile positions and remove merger information
  console.log("Before prepare: ");
  console.log(self.grid.cells);

  self.prepareTiles();

  // console.log(direction)
  console.log("Move type: ", moveType)

  console.log("Before move: ");
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
      // get board
      var json = JSON.parse(request.responseText);
      var updatedCells = json['board'];
      var randomTile = json["newTile"];
      // get metadata
      self.metaData.c_score = request.response;
      self.metaData.c_score = json["c_score"];
      self.metaData.game_over = json["game_over"];

      // DEBUG
      console.log("recieved randomTile  is:  ");
      console.log(randomTile);

      // DEBUG
      console.log("recieved 2D array is:  ");
      console.log(updatedCells);

      var cell, tile;

      // console.log(self.grid.cells);
      var vector     = self.getVector(direction);
      // console.log(vector)
      var traversals = self.buildTraversals(vector);
      var moved      = false;

      // Save the current tile positions and remove merger information

      // Traverse the grid in the right direction and move tiles
      traversals.x.forEach(function (x) {
        traversals.y.forEach(function (y) {
          cell = { x: x, y: y };
          tile = self.grid.cellContent(cell);
          console.log(tile)
          if (tile) {
            var positions = self.findFarthestPosition(cell, vector);
            console.log(cell)
            console.log(vector)

            console.log(position)

            var next      = self.grid.cellContent(positions.next);

            console.log(next)

            // Only one merger per row traversal?
            if (next && next.value === tile.value && !next.mergedFrom) {
              var merged = new Tile(positions.next, tile.value * 2);
              merged.mergedFrom = [tile, next];

              self.grid.insertTile(merged);
              self.grid.removeTile(tile);

              // Converge the two tiles' positions
              tile.updatePosition(positions.next);

              // The mighty 2048 tile
              if (merged.value === 2048) self.won = true;
            } else {
              self.moveTile(tile, positions.farthest);
            }

            if (!self.positionsEqual(cell, tile)) {
              moved = true; // The tile moved from its original cell!
            }
          }
        });
      });
      // console.log(vector);
      // console.log("x: " + traversals.x);
      // console.log("y: " + traversals.y);

      // Add the random tile
      // if (moved) {
      var position = {x: randomTile[1], y: randomTile[2] }
      var randtile = new Tile(position, randomTile[0]);
      self.grid.insertTile(randtile);
      self.actuator.actuate(self.grid, self.metaData);

      console.log("after actuate:")
      console.log(self.grid.cells)
      // }
    }
  };
  // console.log(this.grid);
  //
  // console.log(currentMove)
  request.send(currentMove);

};

GameManager.prototype.moveTile = function (tile, cell) {
  this.grid.cells[tile.x][tile.y] = null;
  this.grid.cells[cell.x][cell.y] = tile;
  tile.updatePosition(cell);
};


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
      console.log(tile)
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
  if (vector.x === 1) traversals.x = traversals.x.reverse();
  if (vector.y === 1) traversals.y = traversals.y.reverse();

  return traversals;
};



// Find the farthers position a cell can go
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

GameManager.prototype.positionsEqual = function (first, second) {
  return first.x === second.x && first.y === second.y;
};
