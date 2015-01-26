
var log = function(d){
    console.log(d);
};
$(document).ready(function() {
    h = document.getElementById('in').onclick = function(){ window.location = "/login";}
    m = document.getElementById('up').onclick = function(){window.location = "/register";}
    n = document.getElementById('out').onclick = function(){window.location = "/logout";}
    o = document.getElementById('userb').onclick = function(){window.location = "/profile/" + document.getElementById("userb").innerHTML;}
});
$('.col-sm-8 col-md-6').click(function() {
    window.location.href = "/loadorders/" + document.getElementByID(/*id*/).innerHTML;
}).css("cursor","pointer");