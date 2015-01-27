var log = function(d){
console.log(d);
};
$(document).ready(function() {
    n = document.getElementById('out').onclick = function(){window.location = "/logout";}
    o = document.getElementById('userb').onclick = function(){window.location = "/profile/" + document.getElementById("userb").innerHTML;}
    p = document.getElementById('placeorder').onclick = function(){window.location = "/placeorder/" + document.getElementById("orderid").innerHTML;}
});

$('.col-sm-8 col-md-6').click(function() {
window.location.href = "http://stackoverflow.com";
}).css("cursor","pointer");
