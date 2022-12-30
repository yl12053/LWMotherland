((px, py, hx) => {
  function shuffle(array) {
    let currentIndex = array.length, randomIndex;
    while (currentIndex != 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
      [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }
    return array;
  }
  setInterval(() => {
    $.ajax({
      "url": "/apis/game1/keep_key_alive",
      "method": "POST",
      "data": {
        "hx": hx
      }
    })
  }, 60000);
  var privkey = nobleSecp256k1.utils.randomPrivateKey();
  var point = nobleSecp256k1.Point.fromPrivateKey(privkey);
  var pointx = point.x;
  var pointy = point.y;
  $.ajax({
    "url": "/apis/game1/ecdhe",
    "method": "POST",
    "data": {
      "hx": hx,
      "px": String(pointx),
      "py": String(pointy)
    },
    "success": (data) => {
      var shared = (new nobleSecp256k1.Point(px, py)).multiply(BigInt("0x"+nobleSecp256k1.utils.bytesToHex(privkey)));
      var shared_key = new BN(shared.x).toString(16).padStart(64, '0');
      var shared_iv = new BN(shared.y).toString(16).padStart(64, '0').slice(0, 32);
      var dFR = 10;
      var perQuestion = 1;
      var timeMult = 1;
      function pQuestion(der, cdobj){
        var corrCount = 0;
        var wrongCount = 0;
        var globMark = 0;
        if ((!window.localStorage.getItem(".q(YPVKM5Re2ADI%C")) || JSON.parse(window.localStorage.getItem(".q(YPVKM5Re2ADI%C")).length != der.length){
          var rlist = [...Array(der.length).keys()];
          rlist = shuffle(rlist);
          window.localStorage.setItem(".q(YPVKM5Re2ADI%C", JSON.stringify(rlist));
        } else {
          var rlist = JSON.parse(window.localStorage.getItem(".q(YPVKM5Re2ADI%C"));
        }
        if ((!window.localStorage.getItem("u9aTDfz($2K%Ev3x")) || JSON.parse(window.localStorage.getItem("u9aTDfz($2K%Ev3x")).length != der.length){
          var btns = Array.from({length: der.length}, (_, i) => shuffle([1,2,3,4]));
          window.localStorage.setItem("u9aTDfz($2K%Ev3x", JSON.stringify(btns));
        } else {
          var btns = JSON.parse(window.localStorage.getItem("u9aTDfz($2K%Ev3x"));
        }
        function selection(btn){
          $("#demo").text(["", "A", "B", "C", "D"][btn]);
          $(".btns").removeClass("activ abut").addClass("abut");
          $("#btn"+["", "1", "2", "3", "4"][btn]).removeClass("abut").addClass("activ");
          $("#btnconfirm").removeClass("dab").addClass("abut");
        }
        var obj = {};
        var arrv = [];
        for (var tempI = 1; tempI <= 4; tempI++){
          obj["incorrect"+tempI] = $("<video muted>").css("width", "80%").append($("<source>").attr("src", "/assets/video/Games/game1/"+tempI+"_incorrect.mp4")).hide();
          obj["incorrect"+tempI][0].load();
          arrv.push(obj["incorrect"+tempI][0]);
          obj["correct"+tempI] = $("<video muted>").css("width", "80%").append($("<source>").attr("src", "/assets/video/Games/game1/"+tempI+"_correct.mp4")).hide();
          obj["correct"+tempI][0].load();
          arrv.push(obj["correct"+tempI][0]);
        }
        $("#cg_container").append($(arrv));
        function questionSet(qnum){
          function atta(num, crt){
            $(arrv).hide();
            obj[crt+num].show();
            obj[crt+num][0].pause();
            obj[crt+num][0].currentTime = 0;
            obj[crt+num][0].play();
            obj[crt+num][0].onended = (() => {cdobj.resume(); questionSet(qnum + 1); obj[crt+num][0].onended = undefined; $("#btnconfirm").show()});
          }
          function finishHandler(timeout, timeoutValue){
            function timeSelector(time){
              if (10 <= time && time <= 20){
                return 2;
              } else if (20 < time && time <= 30){
                return 5;
              } else if (30 < time){
                return 10;
              } else {
                return 0;
              }
            }
            // alert(`Finished with following data:\nTimeout: ${timeout}\nRemaining: ${timeoutValue}\nMarks:${globMark}\nFinal Marks:${globMark + timeSelector(Math.floor(timeoutValue))}`);
            $("#mainzone").hide();
            $("#final").show();
            $("#flagTime").text(""+(!timeout));
            $("#timeLeft").text(""+cdobj.craftTimeString(Math.floor(timeoutValue)));
            $("#mark").text(""+(globMark+timeSelector(Math.floor(timeoutValue))));
            $("#corrCount").text(""+corrCount);
            $("#wrongCount").text(""+wrongCount);
            var ivdTemp = CryptoJs.enc.Hex.parse(shared_iv);
            var ivdBuffer = CryptoJs.SHA256(ivdTemp);
            var ivdHex = CryptoJs.enc.Hex.stringify(ivdBuffer).slice(0, 32);
            var ivdFinal = CryptoJs.enc.Hex.parse(ivdHex);
            var keyFinal = CryptoJs.enc.Hex.parse(shared_key);
            var data = {
              corrCount: corrCount,
              wrongCount: wrongCount,
              timeLeft: Math.floor(timeoutValue),
              mark: globMark+timeSelector(Math.floor(timeoutValue))
            }
            var stData = JSON.stringify(data);
            var encryptedData = CryptoJs.AES.encrypt(stData, keyFinal, {iv: ivdFinal});
            var payload = CryptoJs.enc.Base64.stringify(encryptedData.ciphertext);
            $.ajax({
              "url": "/apis/game1/update",
              "method": "POST",
              "data": {
                payload: payload
              },
              "success": () => {
                $("#map_button").removeClass("wrong");
                $("#map_button").click(() => {window.location = "/map";});
                $("#loadingIcon").hide();
              }
            });
          }
          cdobj.setHandler(() => {
            finishHandler(false, cdobj.getRemains());
          });
          $(".btns").off("click");
          $(".btns").removeClass("activ abut wrong correct wrong_nonexplict").addClass("abut");
          $("#btnconfirm").removeClass("abut").addClass("dab");
          if (qnum == der.length){
            cdobj.pause();
            finishHandler(true, cdobj.getRemains());
          } else {
            var trueNum = rlist[qnum];
            var qobj = der[trueNum];
            $("#question_container").text(qobj[1]);
            var currSel = [undefined];
            btns[qnum].map((btn, shuf) => {$("#btn"+btn).text(qobj[shuf+2]).click(() => {if (cdobj.getRemains() > 0){selection(btn); currSel[0] = btn;}});});
            function correct_handler(selec){
              cdobj.pause();
              cdobj.addSeconds(15);
              $(".btns").addClass("wrong_nonexplict");
              $(".btns.activ").removeClass("activ wrong_nonexplict").addClass("correct");
              atta(selec, "correct");
              globMark += perQuestion;
              corrCount++;
            }
            function incorrect_handler(selec, c, a){
              cdobj.pause();
              cdobj.addSeconds(15);
              $(".btns").addClass("wrong_nonexplict");
              $(".btns.activ").removeClass("activ wrong_nonexplict").addClass("wrong");
              $("#btn"+a).addClass("correct").removeClass("wrong_nonexplict");
              atta(selec, "incorrect");
              wrongCount++;
            }
            $("#btnconfirm").text("Confirm!").click(() => {
              if (currSel[0]){
                if (cdobj.getRemains() > 0){
                  if (btns[qnum].indexOf(currSel[0])+1 == qobj[6]){
                    correct_handler(currSel[0]);
                  } else {
                    incorrect_handler(currSel[0], qobj[6], btns[qnum][qobj[6]-1]);
                  }
                  $("#btnconfirm").text((qnum + 1 == der.length)?"Finish!":"Continue!");
                  $(".btns").off("click").removeClass("abut");
                  $("#btnconfirm").addClass("abut").hide();
                }
              }
            });
          }
        }
        questionSet(0);
        function showQuestion(){
          if (window.pDone){
            $("#mainzone").show();
          } else {
            setTimeout(showQuestion, 0);
          }
        }
        setTimeout(showQuestion, 0);
      }
      function fQuestion(){
        $.ajax({
          "url": "/apis/game1/fetch_q",
          "method": "POST",
          "data": {
            "hx": hx
          },
          "success": (data) => {
            var ivd = CryptoJs.enc.Hex.parse(shared_iv);
            var dec = CryptoJs.AES.decrypt(data, CryptoJs.enc.Hex.parse(shared_key), { iv: ivd });
            try {
              var der = JSON.parse(CryptoJs.enc.Utf8.stringify(dec));
              var cdobj = createCountdown(100, 100, 100, 10, 10);
              cdobj.setCountdownSec(90);
              cdobj.app.view.style.height = "100%";
              cdobj.app.view.style.width = "100%";
              $("#countdown_container")[0].appendChild(cdobj.app.view);
              setTimeout(pQuestion, 0, der, cdobj);
              cdobj.beginCountdown();
            } catch (error){
              dFR--;
              if (dFR > 0){
                setTimeout(fQuestion, 500);
              } else {
                function reLoc(){
                  if (window.pDone){
                    window.location = "/Game1?cg=0";
                  } else {
                    setTimeout(reLoc, 0);
                  }
                }
                setTimeout(reLoc, 0);
              }
            }
          }
        });
      }
      setTimeout(fQuestion, 0);
    }
  });
})(BigInt("{{ px }}"), BigInt("{{ py }}"), "{{ hx }}");