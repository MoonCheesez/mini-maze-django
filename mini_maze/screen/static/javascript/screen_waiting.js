$(document).ready(function() {
    // Set the colour of the number of players left
    var colours = ["#FFB98B", "#FFBAE4", "#C491F1", "#00CDF1"];
    
    var playersLeftDOM = document.getElementById("players-left");
    var playersLeft = parseInt(playersLeftDOM.textContent);
    
    var colour = colours[playersLeft-1];
    playersLeftDOM.style.color = colour;

    playersLeftDOM.className = "pop-in";
    playersLeftDOM.style.visibility = "visible";

    // Check for updates
    window.setInterval(function() {
        var newPlayersLeft;
        $.getJSON("/players", function(d) {
            var tmp = d["players_joined"];
            //tmp.count(false)
            newPlayersLeft = tmp.reduce(function(total,x){return x==false ? total+1 : total}, 0);
            if (newPlayersLeft != playersLeft && newPlayersLeft != 0) {
                function changeAndPopOut() {
                    playersLeft = newPlayersLeft;
                    // pluralize 'players' if needed
                    if (playersLeft > 1) {
                        document.getElementById("more-players").textContent = "players";
                    } else {
                        document.getElementById("more-players").textContent = "player";
                    }

                    playersLeftDOM.textContent = playersLeft.toString();
                    playersLeftDOM.style.color = colours[playersLeft-1];
                    playersLeftDOM.className = "pop-in";
                }

                playersLeftDOM.addEventListener("animationend", changeAndPopOut, false);
                playersLeftDOM.addEventListener("webkitAnimationEnd", changeAndPopOut, false);
                playersLeftDOM.addEventListener("MSAnimationEnd", changeAndPopOut, false);
                
                playersLeftDOM.className = "pop-out";
            } else if (newPlayersLeft == 0) {
                function popOut() {
                    document.getElementById("waiting").style.visibility = "hidden";
                    playersLeftDOM.style.visibility = "visible";
                    playersLeftDOM.textContent = "START!";
                    playersLeftDOM.style.color = "#F58081";
                    playersLeftDOM.className = "pop-in";
                    setTimeout(function() {window.location.reload()}, 300);
                }

                playersLeftDOM.addEventListener("animationend", popOut, false);
                playersLeftDOM.addEventListener("webkitAnimationEnd", popOut, false);
                playersLeftDOM.addEventListener("MSAnimationEnd", popOut, false);

                playersLeftDOM.className = "pop-out";
            }
        });

    }, 500);
});