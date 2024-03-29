((px, py, hx) => {
  var actObj = {}
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
      var perQuestion = 10;
      var timeMult = 1;
      function pQuestion(der, cdobj){
        var corrCount = {{ ccount }};
        var wrongCount = {{ wcount }};
        var globMark = {{ ccount }} * perQuestion;
        if ((!window.localStorage.getItem(".q(YPVKM5Re2ADI%C")) || JSON.parse(window.localStorage.getItem(".q(YPVKM5Re2ADI%C")).length != der.length){
          var rlist = [...Array(der.length).keys()];
          rlist = shuffle(rlist);
          window.localStorage.setItem(".q(YPVKM5Re2ADI%C", JSON.stringify(rlist));
        } else {
          var rlist = JSON.parse(window.localStorage.getItem(".q(YPVKM5Re2ADI%C"));
        }
        if ((!window.localStorage.getItem("u9aTDfz($2K%Ev3x")) || JSON.parse(window.localStorage.getItem("u9aTDfz($2K%Ev3x")).length != der.length){
          //var btns = Array.from({length: der.length}, (_, i) => shuffle([1,2,3,4]));
          var btns = Array.from({length: der.length}, (_, i) => [1,2,3,4]);
          window.localStorage.setItem("u9aTDfz($2K%Ev3x", JSON.stringify(btns));
        } else {
          // var btns = JSON.parse(window.localStorage.getItem("u9aTDfz($2K%Ev3x"));
          var btns = Array.from({length: der.length}, (_, i) => [1,2,3,4]);
          window.localStorage.setItem("u9aTDfz($2K%Ev3x", JSON.stringify(btns));
        }
        function selection(btn){
          $("#demo").text(["", "A", "B", "C", "D"][btn]);
          $(".btns").removeClass("activ abut").addClass("abut");
          $("#btn"+["", "1", "2", "3", "4"][btn]).removeClass("abut").addClass("activ");
          $(".btnccf").removeClass("dab").addClass("abut");
        }
        var obj = {};
        var arrv = [];
        for (var tempI = 1; tempI <= 4; tempI++){
          obj["incorrect"+tempI] = $("<video muted>").css("width", "100%").append($("<source>").attr("src", assets_url +　"/video/Games/game1/"+tempI+"_incorrect.mp4")).prop("defaultPlaybackRate", 2).hide();
          obj["incorrect"+tempI][0].load();
          arrv.push(obj["incorrect"+tempI][0]);
          obj["correct"+tempI] = $("<video muted>").css("width", "100%").append($("<source>").attr("src", assets_url +　"/video/Games/game1/"+tempI+"_correct.mp4")).prop("defaultPlaybackRate", 2).hide();
          obj["correct"+tempI][0].load();
          arrv.push(obj["correct"+tempI][0]);
        }
        $("#videoCont").append($(arrv));
        function questionSet(qnum){
          function atta(num, crt){
            $(arrv).hide();
            obj[crt+num].show();
            obj[crt+num][0].pause();
            obj[crt+num][0].currentTime = 0;
            obj[crt+num][0].play();
            obj[crt+num][0].onended = (() => {cdobj.resume(); questionSet(qnum + 1); obj[crt+num][0].onended = undefined; $(".btnccf").show()});
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
          $(".btnccf").removeClass("abut").addClass("dab");
          if (qnum == der.length){
            cdobj.pause();
            finishHandler(true, cdobj.getRemains());
          } else {
            var trueNum = rlist[qnum];
            var qobj = der[trueNum];
            $("#question_container").text((qnum+1)+". "+qobj[1]);
            var currSel = [undefined];
            btns[qnum].map((btn, shuf) => {
              $("#inner"+btn).css("font-size", '24px');
              $("#inner"+btn).text(qobj[shuf+2]).parent().click(() => {if (cdobj.getRemains() > 0){selection(btn); currSel[0] = btn;}});
              function tr(){
                if (document.querySelector("#inner"+btn).scrollHeight == 0){
                  setTimeout(tr, 0);
                } else {
                  function g2(){
                    if (document.querySelector("#inner"+btn).scrollHeight > $("#inner"+btn).prop("clientHeight")){
                      //console.log(btn);
                      $("#inner"+btn).css("font-size", parseInt($("#inner"+btn).css("font-size"))*3/4 + "px");
                      setTimeout(g2, 5);
                    }
                  }
                  setTimeout(g2, 0);
                }
              }
              setTimeout(tr, 0);
            });
            function hand_med(tr, sel){
              var selAns = btns[qnum].indexOf(sel)+1;
              var obj = {
                "q": tr,
                "sel": selAns,
                "t": Math.ceil(cdobj.getRemains()),
              };
              var ivdTemp = CryptoJs.enc.Hex.parse(shared_iv);
              var ivdBuffer = CryptoJs.SHA256(ivdTemp);
              shared_iv = CryptoJs.enc.Hex.stringify(ivdBuffer).slice(0, 32);
              var ivdFinal = CryptoJs.enc.Hex.parse(shared_iv);
              var keyFinal = CryptoJs.enc.Hex.parse(shared_key);
              var stData = JSON.stringify(obj);
              var encryptedData = CryptoJs.AES.encrypt(stData, keyFinal, {iv: ivdFinal});
              var payload = CryptoJs.enc.Base64.stringify(encryptedData.ciphertext);
              $.ajax({
                "url": "/apis/game1/middleHandler",
                "method": "POST",
                "data": {
                  "hx": hx,
                  "payload": payload
                }
              });
            }
            function correct_handler(selec){
              cdobj.pause();
              // cdobj.addSeconds(15);
              $(".btns").addClass("wrong_nonexplict");
              $(".btns.activ").removeClass("activ wrong_nonexplict").addClass("correct");
              atta(selec, "correct");
              globMark += perQuestion;
              corrCount++;
              setTimeout(hand_med, 0, trueNum, selec);
            }
            function incorrect_handler(selec, c, a){
              cdobj.pause();
              // cdobj.addSeconds(15);
              $(".btns").addClass("wrong_nonexplict");
              $(".btns.activ").removeClass("activ wrong_nonexplict").addClass("wrong");
              $("#btn"+a).addClass("correct").removeClass("wrong_nonexplict");
              atta(selec, "incorrect");
              wrongCount++;
              setTimeout(hand_med, 0, trueNum, selec);
            }
            $(".corn").text("✓").css("background-color", "#217845");
            $("#leftmain").css("background-color", "#38C871");
            $("#rightmain").css("background-color", "#38C871");
            // $("#leftmain").css("background-color", "")
            for (var vari of ["#leftmain", "#rightmain"]){
              $(vari).text("Confirm").parent().click(() => {
                if (currSel[0]){
                  if (cdobj.getRemains() > 0){
                    if (btns[qnum].indexOf(currSel[0])+1 == qobj[6]){
                      correct_handler(currSel[0]);
                      $("#leftmain").text("Correct");
                      $("#rightmain").text("Correct");
                    } else {
                      incorrect_handler(currSel[0], qobj[6], btns[qnum][qobj[6]-1]);
                      $(".corn").text("✗").css("background-color", "#782421");
                      $("#leftmain").css("background-color", '#C83200');
                      $("#rightmain").css("background-color", '#C83200');
                      $("#leftmain").text("Wrong");
                      $("#rightmain").text("Wrong");
                    }
                    
                    $(".btns").off("click").removeClass("abut");
                    $(".btnccf").off("click").removeClass("abut");
                  }
                }
              });
            }
          }
        }
        questionSet({{ fq }});
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
              var ctdv = {{ cdv }};
              cdobj.setCountdownSec(ctdv);
              cdobj.app.view.style.height = "100%";
              cdobj.app.view.style.width = "100%";
              $("#countdown_container")[0].appendChild(cdobj.app.view);
              setTimeout(pQuestion, 0, der, cdobj);
              cdobj.beginCountdown();
              window.cdo = cdobj;
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