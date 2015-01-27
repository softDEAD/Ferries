
var log = function(d){
		console.log(d);
};

$(document).ready(function() {
    h = document.getElementById('in').onclick = function(){ window.location = "/login";}
    m = document.getElementById('up').onclick = function(){window.location = "/register";}
});

$('.col-sm-8 col-md-6').click(function() { 
    window.location.href = "http://stackoverflow.com";
}).css("cursor","pointer");

