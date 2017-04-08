// Function to set the player positions into HTML
function setPlayerPosition(player_value, player_pos) {
    var x = player_pos[0];
    var y = player_pos[1];

    document.getElementById("maze").getElementsByTagName("tr")[y]
        .getElementsByTagName("td")[x].setAttribute("id", player_value);
}

function movePlayer(player_value, from, to) {
    setPlayerPosition("", from);
    setPlayerPosition(player_value, to);
}

function getNextLocation(move, currentPos) {
    // Moves the player and returns that location
    var dx = [0, -1, 1, 0];
    var dy = [-1, 0, 0, 1];

    var nx = currentPos[0] + dx[move-1];
    var ny = currentPos[1] + dy[move-1];

    if (nx >= 0 && ny >= 0) {
        return [nx, ny];
    } else {
        return currentPos;
    }
}

function displayString(value) {
    setTimeout(function() {
        document.getElementById("current-move").innerHTML = "";
    }, 500);
    document.getElementById("current-move").innerHTML = value;
}

function getPlayerMoving(move_num) {
    if (move_num == 0) {
        return 1;
    } else {
        return [4, 1, 2, 3][move_num];
    }
}

var startup = true;

var playerPositions = [null, null, null, null];
var playerValues = ["player1", "player2", "player3", "player4"];

var moves = [];
var moveTypes = ["move_up", "move_left", "move_right", "move_down"];
var playerMoving;

var data;
$(document).ready(function() {
    // Setup
    $.getJSON("/players", function(d) {
        playerMoving = d["moves"][0]
        // Draw players
        for (var i=0; i<4; i++) {
            var newPosition = d["player_positions"][i];
            setPlayerPosition(playerValues[i], newPosition);
            playerPositions[i] = newPosition;
        };

        // Show center
        var rows = document.getElementById("maze").getElementsByTagName("tr");
        var x = rows.length/2;
        var y = rows[0].getElementsByTagName("td").length/2;
        setPlayerPosition("center", [x, y]);
        setPlayerPosition("center", [x-1, y]);
        setPlayerPosition("center", [x, y-1]);
        setPlayerPosition("center", [x-1, y-1]);

        // Show player's turn
        document.getElementById("player-move-text").textContent = getPlayerMoving(d["move_number"]);

        // Show maze
        var maze = d["maze"];
        for (var y = maze.length - 1; y >= 0; y--) {
            for (var x = maze[y].length - 1; x >= 0; x--) {
                if (maze[y][x] == 0) {
                    setPlayerPosition("showmaze", [x, y]);
                };
            };
        };
    });

    window.setInterval(function() {
        $.getJSON("/players", function(d) {
            if (startup) {
                moves = d["moves"];
                
                if (moves.length > 0 && moves[0] != playerMoving) {
                    moves = d["moves"];
                    playerMoving = getPlayerMoving(d["move_number"]);
                    startup = false;
                }

            } else if (moves.length > 0) {
                move = moves.shift();

                var currentPosition = playerPositions[playerMoving-1];
                var nextPosition = getNextLocation(move, currentPosition);

                movePlayer(playerValues[playerMoving-1],
                    currentPosition, nextPosition);
                
                // Set new location
                playerPositions[playerMoving-1] = nextPosition;

                displayString(moveTypes[Math.abs(move)-1]);
            } else if (playerMoving != getPlayerMoving(d["move_number"])) {
                moves = d["moves"];
                playerMoving = getPlayerMoving(d["move_number"]);
            } else {
                displayString("");
                // Show player's turn
                document.getElementById("player-move-text").textContent = getPlayerMoving(d["move_number"]);
            }
        });
    }, 1000);
});