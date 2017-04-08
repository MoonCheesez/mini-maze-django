var colors = ["#FFB98B", "#FFBAE4", "#C491F1", "#00CDF1"];

function addAnimationEnd(DOM, fn) {
    DOM.addEventListener("animationend", fn, false);
    DOM.addEventListener("webkitAnimationEnd", fn, false);
    DOM.addEventListener("MSAnimationEnd", fn, false);
}

function setTextColor(DOM, text, color) {
    DOM.textContent = text;
    DOM.style.color = color;
}

function count(list, item) {
    return list.reduce(function(total,x){return x==item ? total+1 : total}, 0)
}

$(document).ready(function() {
    var playersLeftDOM = document.getElementById("players-left");
    var playersTextDOM = document.getElementById("players-text");

    var playersLeft = parseInt(playersLeftDOM.textContent);
    playersLeftDOM.style.color = colors[playersLeft-1];

    playersLeftDOM.className = "pop-in";
    playersLeftDOM.style.visibility = "visible";

    // Check for updates
    var interval = window.setInterval(function() {
        $.getJSON("/players", function(d) {
            var newPlayersLeft = count(d["players_joined"], false);

            if (newPlayersLeft != playersLeft && newPlayersLeft != 0) {
                playersLeft = newPlayersLeft;

                function changeAndPopOut() {
                    // pluralize 'players' if needed
                    playersTextDOM.textContent = playersLeft > 1? "players":"player";

                    setTextColor(playersLeftDOM, playersLeft, colors[playersLeft-1]);
                    playersLeftDOM.className = "pop-in";
                }

                addAnimationEnd(playersLeftDOM, changeAndPopOut);
                playersLeftDOM.className = "pop-out";
            } else if (newPlayersLeft == 0) {
                function popOut() {
                    document.getElementById("waiting").style.visibility = "hidden";
                    
                    setTextColor(playersLeftDOM, "START!", "#F58081");
                    playersLeftDOM.className = "pop-in";
                    playersLeftDOM.style.visibility = "visible";
                    setTimeout(function() {window.location.reload()}, 300);
                }

                addAnimationEnd(playersLeftDOM, popOut);
                playersLeftDOM.className = "pop-out";

                window.clearInterval(interval);
            }
        });
    }, 500);;
});