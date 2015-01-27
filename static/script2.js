var log = function(d){
console.log(d);
};

function getval() {
    var currentTime = new Date()
    var hours = currentTime.getHours()
    var minutes = currentTime.getMinutes()

    if (minutes < 10)
        minutes = "0" + minutes;

    var suffix = "AM";
    if (hours >= 12) {
        suffix = "PM";
        hours = hours - 12;
    }
    if (hours == 0) {
        hours = 12;
    }
    var current_time = hours + ":" + minutes + " " + suffix;
    document.getElementById("clock") = current_time;
}

$(document).ready(function() {
    n = document.getElementById('out').onclick = function(){window.location = "/logout";}
    o = document.getElementById('userb').onclick = function(){window.location = "/profile/" + document.getElementById("userb").innerHTML;}
    p = document.getElementById('placeorder').onclick = function(){window.location = "/placeorder/" + document.getElementById("orderid").innerHTML;}
    w = document.getElementById('yelp').onclick = function(){window.location = "/results";}
});

onload=getval(); 
setinterval('getval()',200)

$('.col-sm-8 col-md-6').click(function() {
window.location.href = "http://stackoverflow.com";
}).css("cursor","pointer");
