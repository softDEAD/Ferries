var s=document.getElementById("Search");
var r=document.getElementById("result");
var geo = document.getElementById('geo').checked;
var log = function(d){
    console.log(d);
};

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

var search = function(){
    if(geo){
	getLocation();
    }else{
	place();
    }
};
var generate= function(result){
    for(var i in result[businessess].keys()){
	r.innerHTML+='<ul class="list-inline"><li><a href='+i["url"]+
	    '<img alt='+i["name"]+'  height="90" width="90" src = '+
	    i["image_url"]+'></a></li><li><a href='+i["url"]+'>'+i["name"]+'<br></a></li><li>Phone Number:'+ i["display_phone"]+'<br>Neighborhood:'+ i["location"]["display_address"][-2]+'<br>Address:';
	for(var h in i["location"]["display_address"]){    
	    r.innerHTML+=h+'<br>';
	}
	r.innerHTML+=i["location"]["display_address"][-1]+'</li>>';
    }
var place= function(){
    var sform = document.getElementById('search-form');
    var loc = document.getElementById('loc').value;
    flash(loc);
    $.ajax({
	type:"POST",
	url:"/results",
	data:'loc='+loc,
	success: function (results) {
	    generate(results)
	},
	error: function(error){
	    console.log(error);
	}
    });
};
var getLocation= function(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition,errorHandler,{enableHighAccuracy:true});
    }else{
        flash("Geolocation is not supported by this browser.");
    }
};

var showPosition= function(position) {
    var term = document.getElementById('term').value;
    $.ajax({
	type:"POST",
	url:"/results",
	data:'lat='+position.coords.latitude+
	    '&lon='+position.coords.longitude+
	    '&term='+term+
	    '&geo='+geo,
	success: function (result) {
	    console.log("success");
	},
	error: function(error){
	    console.log(error);
	}
    });
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

$(document).ready(function() {
    h = document.getElementById('in').onclick = function(){ window.location = "/login";}
    m = document.getElementById('up').onclick = function(){window.location = "/register";}
    s.addEventListener('click', search);
});



