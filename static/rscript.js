var lat=document.getElementById("lat");
var lon=document.getElementById("lon");
var geo = document.getElementById('geo').checked;

var clear=function(){
    var f = document.getElementById("errors");
    for(var i=0;i<f.length;i++){
	f(i).remove();
    }
};

var flash=function(d){
    var f = document.getElementById("errors");
    var newitem = document.createElement('li');
    newitem.innerHTML=d;
    newitem.className="flashed_message error";
    f.appendChild(newitem);
};

var getLocation= function(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition,errorHandler);
    }else{
        flash("Geolocation is not supported by this browser.");
    }
};

var showPosition= function(position) {
    lon.value= position.coords.latitude;
    lat.value= position.coords.longitude;
    console.log(lon.value);
    console.log(lat.value);
};

var errorHandler=function(d) {
    if (d.code == 1) {
	flash("Location access denied");
    }else if(d.code == 2){
	flash("Location can not be determined");
    }else if(d.code == 3){
	flash("Location retrieval timed out");
    }else{
	flash("Unknown error. Did not retrieve location");
    }
};
var startit = function (e) {
    getLocation();
    if (!document.getElementById('geo').checked) {
	stopit;
    }else{
	myevent = setInterval(getLocation,5000);
    }
}

var stopit = function(e) {
    window.clearTimeout(myevent);
}
$(document).ready(function() {
     document.getElementById('geo').addEventListener("click",startit);
});



