$(document).ready(function() {
    // Set the colour of the number of players left
    var colours = ["#FFB98B", "#FFBAE4", "#C491F1", "#00CDF1"];
    
    var playersLeftDOM = document.getElementById("players-left");
    var playersLeft = parseInt(playersLeftDOM.textContent);
    
    var colour = colours[playersLeft-1];
    playersLeftDOM.style.color = colour;

    playersLeftDOM.style.visibility = "visible";

    // Check for updates
    var playersJoined;
    window.setInterval(function() {
        var newPlayersJoined;
        $.getJSON("/players", function(d) {
            var tmp = d["players_joined"];
            //tmp.count(true)
            newPlayersJoined = tmp.reduce(function(total,x){return x==true ? total+1 : total}, 0);
        });

        if (newPlayersJoined != playersJoined) {
            // animate
            playersJoined = newPlayersJoined;
            document.getElementById("players-left").textContent = playersJoined.toString;
        }

    }, 500);
});