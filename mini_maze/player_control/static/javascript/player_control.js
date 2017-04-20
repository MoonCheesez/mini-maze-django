var player_no;
var players = ["player1", "player2", "player3", "player4"];

function setCellButtonClass(pos, buttonClass) {
    var x = pos[0];
    var y = pos[1];
    var grid = document.getElementById("maze-grid");
    var row = grid.getElementsByTagName("tr")[y];
    var col = row.getElementsByTagName("td")[x];
    col.getElementsByTagName("button")[0].className = buttonClass;
}

function movePlayer(oldPos, newPos) {
    setCellClass(oldPos, "");
    setCellClass(newPos, players[player_no-1]);
}

var grid, gridx, gridy;

var currentPos;
$(document).ready(function() {
    var player_noString = document.getElementById("player-no").innerText;
    player_no = parseInt(player_noString[player_noString.length-1]);
    grid = document.getElementById("maze-grid");
    gridy = grid.getElementsByTagName("tr").length;
    gridx = grid.getElementsByTagName("tr")[0].getElementsByTagName("td").length;

    setCellButtonClass([0, 0], players[player_no-1]);
    // Set legend colour
    document.getElementById("player-legend").className = players[player_no-1];
});
