var players = ["player1", "player2", "player3", "player4"];

function Path(path) {
    this.path = path;
    this.draw = function(pos1, pos2) {
        function getJoint(pos, joint_num) {
           return getGridButton(pos).getElementsByClassName("joint" + joint_num.toString())[0];
        }


        // Joint 1 is the "from" joint
        // Joint 2 is the "to" joint
        var pos1Joint2 = getJoint(pos1, 2);
        var pos2Joint1 = getJoint(pos2, 1);

        // Access the keys by x then y
        // Get the values of x and y by pos1 - pos2
        var pos1Key = [[null, "from-right"], ["from-bottom", null, "from-top"], [null, "from-left"]];
        var pos2Key = [[null, "from-left"], ["from-top", null, "from-bottom"], [null, "from-right"]];
        
        var x_diff = pos1[0] - pos2[0];
        var y_diff = pos1[1] - pos2[1];

        pos1Joint2.className = "joint2 " + pos1Key[x_diff+1][y_diff+1];
        pos2Joint1.className = "joint1 " + pos2Key[x_diff+1][y_diff+1];

        pos1Joint2.style.display = "initial";
        pos2Joint1.style.display = "initial";
    }
    this.add = function(nextPos) {
        var previousPos = this.last();
        this.draw(previousPos, nextPos);
        this.path.push(nextPos);
    }
    this.addVector = function(pos, vector) {
        // This process ensures both pos and vector are not affected
        var x = vector[0];
        var y = vector[1];

        var newPos = [];
        newPos[0] = pos[0];
        newPos[1] = pos[1];
        newPos[0] += x;
        newPos[1] += y;
        return newPos;
    }
    this.moveWith = function(moveVector) {
        var nextPos = this.addVector(this.last(), moveVector);
        this.draw(this.last(), nextPos);
        this.path.push(nextPos);
    }
    this.canMoveWith = function(moveVector) {
        var nextPos = this.addVector(this.last(), moveVector);

        function withinGrid(pos) {
            return pos[0] >= 0 && pos[0] < gridx && pos[1] >= 0 && pos[1] < gridy;
        }

        function notBlocked(pos) {
            return !getGridButton(pos).className.includes("blocked"); 
        }

        function notBeenThere(path, pos) {
            var flag = true;
            for (var i = 0; i < path.length; i++) {
                if (path[i].toString() == pos.toString()) {
                    flag = false;
                }
            }
            return flag;
        }

        return withinGrid(nextPos) && notBlocked(nextPos) && notBeenThere(this.path, nextPos);
    }
    this.last = function() {
        return this.path[this.path.length-1];
    }
    this.highlight = function(index) {
        getGridButton(this.path[index]).className = "pathHighlight";
    }
    this.unhighlight = function(index) {
        getGridButton(this.path[index]).className = "";
    }
    this.move = function() {
        this.path = [this.last()];
    }
}

function getGridCell(pos) {
    var x = pos[0];
    var y = pos[1];
    var grid = document.getElementById("maze-grid");
    return grid.getElementsByTagName("tr")[y].getElementsByTagName("td")[x];
}

function getGridButton(pos) {
    return getGridCell(pos).getElementsByTagName("button")[0];
}

/* Movement buttons */
function addCommand(command) {
    var commandBox = document.getElementById("command-box");
    var ol = commandBox.getElementsByTagName("ol")[0];
    var commandNum = ol.getElementsByTagName("li").length;
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(command));
    li.id = "command" + commandNum.toString();
    li.onclick = function () {
        var commandNum = parseInt(this.id[this.id.length-1]);
    }
    ol.appendChild(li);
}
function buttonMove(moveVector, command) {
    if (path.canMoveWith(moveVector)) {
        path.moveWith(moveVector);
        addCommand(command);
    } else {
        console.log("nope");
    }
}

function moveUp() {
    var moveVector = [0, -1];
    buttonMove(moveVector, "move_up()");
}

function moveDown() {
    var moveVector = [0, 1];
    buttonMove(moveVector, "move_down()");
}

function moveLeft() {
    var moveVector = [-1, 0];
    buttonMove(moveVector, "move_Left()");
}

function moveRight() {
    var moveVector = [1, 0];
    buttonMove(moveVector, "move_right()");
}

function sendCommands() {
    
}

var grid, gridx, gridy;
var path;
var currentPos;
$(document).ready(function() {
    grid = document.getElementById("maze-grid");
    gridy = grid.getElementsByTagName("tr").length;
    gridx = grid.getElementsByTagName("tr")[0].getElementsByTagName("td").length;

    var player_noString = document.getElementById("player-no").innerText;
    var player_no = parseInt(player_noString[player_noString.length-1]);
    var playerClass = players[player_no-1];

    // Set legend colour
    document.getElementById("player-legend").className = playerClass;


    path = new Path([[0, 0]]);
});