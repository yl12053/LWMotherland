var btns = [
  [813, 903, () => {}, function(event){alert('Yangtze');}],
  [1037, 949, function(event){window.clickable=false;bhole(1037, 949, function(){$.ajax(
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
  )}, function(){window.location="/Game1?cg=1";});}],
  [1327, 1335, () => {},  function(event){alert('hk');}],
  [1317, 615, () => {}, function(event){alert('Forbidden City');}]
];