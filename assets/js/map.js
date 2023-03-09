var btns = [
  [1002, 911, function(event){window.clickable=false;bhole(1033, 936, function(){$.ajax(
    {
      "url": "/changeLoc",
      "method": "POST",
      "data": {
        "dim": 1,
        "x": -1,
        "y": -1,
        "reserved": 0
      },
      "success": function(data){
        if (data == "Success"){
          window.locked = false;
        } else{
          alert("Error occurred");
          location.reload();
        }
      }
    }
  )}, function(){window.location="/Game1?cg=1";});},assets_url + "/images/map/button1.jpg", assets_url + "/images/map/y1.jpg"],
  [796, 867, function(event){window.clickable=false;bhole(827, 894, function(){$.ajax(
    {
      "url": "/changeLoc",
      "method": "POST",
      "data": {
        "dim": 2,
        "x": -1,
        "y": -1,
        "reserved": 0
      },
      "success": function(data){
        if (data == "Success"){
          window.locked = false;
        } else {
          alert("Error occurred");
          location.reload();
        }
      }
    }
  )}, function(){window.location="/Game2?cg=1";});},assets_url + "/images/map/button2.jpg", assets_url + "/images/map/y2.jpg"],
  [1283, 578, function(event){window.clickable=false;bhole(1314, 603, function(){$.ajax(
    {
      "url": "/changeLoc",
      "method": "POST",
      "data": {
        "dim": 3,
        "x": -1,
        "y": -1,
        "reserved": 0
      },
      "success": function(data){
        if (data == "Success"){
          window.locked = false;
        } else {
          alert("Error occurred");
          location.reload();
        }
      }
    }
  )}, function(){window.location="/Game3?cg=1";});},assets_url + "/images/map/button3.jpg", assets_url + "/images/map/y3.jpg"]
];