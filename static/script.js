
var log = function(d){
		console.log(d);
};

var getval = function(e) {
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
    h = document.getElementById('in').onclick = function(){ window.location = "/login";}
    m = document.getElementById('up').onclick = function(){window.location = "/register";}
    p = document.getElementById('yelp').onclick = function(){window.location = "/results";}
});

var onload = setinterval(getval(),200)


$('.col-sm-8 col-md-6').click(function() { 
    window.location.href = "http://stackoverflow.com";
}).css("cursor","pointer");

