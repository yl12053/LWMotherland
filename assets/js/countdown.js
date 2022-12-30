function createCountdown(x2, y2, radius, w, col){
  var timeoutHandler = [(() => {})];
  function craftTimeString(t){
    t = Math.floor(t);
    var m = Math.floor(t / 60);
    var s = t % 60;
    var rt = "";
    if (m < 10){
      rt += "0";
    }
    rt += m + ":";
    if (Math.ceil(s) < 10){
      rt += "0";
    }
    rt += Math.ceil(s);
    return rt;
  }
  function getGradientGeneral(ratio, color1, color2){
    var hex = function(x) {
        x = x.toString(16);
        return (x.length == 1) ? '0' + x : x;
    };

    var r = Math.ceil(parseInt(color1.substring(0,2), 16) * ratio + parseInt(color2.substring(0,2), 16) * (1-ratio));
    var g = Math.ceil(parseInt(color1.substring(2,4), 16) * ratio + parseInt(color2.substring(2,4), 16) * (1-ratio));
    var b = Math.ceil(parseInt(color1.substring(4,6), 16) * ratio + parseInt(color2.substring(4,6), 16) * (1-ratio));

    return (r << 16) + (g << 8) + b;
  }
  
  function getGradientByProc(proc){
    if (proc <= 0.25){
      var nproc = 1 - proc / 0.25;
      return getGradientGeneral(nproc, "8A9B0F", "F8CA00");
    } else if (proc <= 0.5){
      var nproc = 1 - (proc - 0.25) / 0.25;
      return getGradientGeneral(nproc, "F8CA00", "E97F02");
    } else if (proc <= 0.75){
      var nproc = 1 - (proc - 0.5) / 0.25;
      return getGradientGeneral(nproc, "E97F02", "BD1550");
    } else {
      var nproc = 1 - (proc - 0.75) / 0.25;
      return getGradientGeneral(nproc, "BD1550", "490A3D");
    }
  }
  var x = radius;
  var y = radius;
  var app = new PIXI.Application({ width: radius * 2, height: radius * 2 , transparent: true, backgroundAlpha: 0});
  var lstyle = new PIXI.LineStyle({width: col});
  var countdowns = 0;
  var stopped = true;
  var intermediate = 0;
  
  var text = new PIXI.Text('', {
     fontFamily: "consolas",
     fill: 0x000000,
     align: 'center'
  });
  text.anchor.set(0.5);
  text.style.fontSize = radius * 9 / 20;
  text.x = radius;
  text.y = radius;
  
  var circle = new PIXI.Sprite();
  circle.x = 0;
  circle.y = 0;
  app.stage.addChild(circle);
  app.stage.addChild(text);
  
  function drawD(degree, x, y, radius, w, col, color){
    var gr = new PIXI.Graphics();
    gr.beginFill(0xC0C0C0);
    gr.drawCircle(x, y, radius);
    gr.beginFill(getGradientByProc(color));
    gr.lineStyle(0);
    gr.arc(x, y, radius, -Math.PI/2, degree * Math.PI / 180 - Math.PI / 2);
    gr.arc(x, y, radius-w, degree * Math.PI / 180 - Math.PI / 2, -Math.PI/2);
    gr.beginFill(0xFFFFFF);
    gr.drawCircle(x, y, radius - w);
    gr.endFill();

    var texture = app.renderer.generateTexture(gr);
    circle.texture = texture;
  }
  var remains = 0;
  function setCountdownSec(s){
    countdowns = s;
    intermediate = s;
    remains = s;
    text.text = craftTimeString(s);
    drawD(360, x, y, radius, w, col, 0);
  }
  var deg = 360;
  var nowTime = +(new Date());
  var nextTime = +(new Date());
  var news = 0;
  function generalC(oldtime){
    if (!stopped){
      var t = +(new Date())
      var orem = remains;
      remains -= (t - oldtime)/1000;
      if (Math.floor(orem) != Math.floor(remains)){
        text.text = craftTimeString(remains);
      }
      if (remains > 0){
        setTimeout(generalC, 0, t);
      }
    }
  }
  function beginCountdown(){
    stopped = false;
    deg = 360;
    var step = countdowns/360;
    nowTime = +(new Date());
    nextTime = +(new Date());
    function f(){
      if (!stopped){
        if (+new Date() < nextTime){
          setTimeout(f, 0);
        } else {
          var progress = 1 - remains / countdowns;
          drawD(deg, x, y, radius, w, col, progress);
          intermediate -= step;
          deg--;
          if (deg >= 0){
            nextTime += step * 1000;
            setTimeout(f, 0);
          } else {
            remains = 0;
            text.text = "00:00";
            stopped = true;
            timeoutHandler[0]();
          }
        }
      }
    }
    setTimeout(f, 0);
    setTimeout(generalC, 0, nowTime);
  }
  
  function pause(){
    stopped = true;
    intermediate = remains;
  }
  
  function setnow(t){
    nowTime = t;
  }
  
  function addSeconds(s){
    if (!stopped){
      pause();
    }
    remains += s;
    intermediate = remains;
    var nowDegree = intermediate / countdowns * 360;
    drawD(nowDegree, x, y, radius, w, col, 1 - remains/countdowns);
    text.text = craftTimeString(remains);
  }
  
  function deltaIntermediate(delta){
    intermediate += delta;
  }
  
  function resume(){
    var nowDegree = intermediate / countdowns * 360;
    var nextintdeg = Math.floor(nowDegree);
    drawD(nowDegree, x, y, radius, w, col, 1 - intermediate/countdowns);
    var degdiff = nowDegree - nextintdeg;
    var step = countdowns/360;
    var timdiff = degdiff * step;
    intermediate = (nextintdeg + 1) * step;
    deg = nextintdeg;
    function f(){
      if (!stopped){
        if (+new Date() < nextTime){
          setTimeout(f, 0);
        } else {
          var progress = 1 - remains / countdowns;
          drawD(deg, x, y, radius, w, col, progress);
          deltaIntermediate(-step);
          deg--;
          if (deg >= 0){
            nextTime += step * 1000;
            setTimeout(f, 0);
          } else {
            remains = 0;
            text.text = "00:00";
            stopped = true;
            timeoutHandler[0]();
          }
        }
      }
    }
    stopped = false;
    setTimeout(generalC, 0, +(new Date()));
    setTimeout(() => {
      setnow(+(new Date()));
      nextTime = +(new Date());
      setTimeout(f, 0);
    }, timdiff * 1000);
  }
  
  function getIntermediate(){
    return intermediate;
  }
  
  return {
    "app": app,
    "setCountdownSec": setCountdownSec,
    "beginCountdown": beginCountdown,
    "getRemains": () => {return remains;},
    "pause": pause,
    "resume": resume,
    "addSeconds": addSeconds,
    "setHandler": ((handler) => {timeoutHandler[0] = handler;}),
    "craftTimeString": craftTimeString
  }
}