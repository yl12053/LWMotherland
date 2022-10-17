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
      var shared_key = new BN(shared.x).toString(16);
      var shared_iv = new BN(shared.y).toString(16).slice(0, 32);
      var dFR = 10;
      function pQuestion(der){
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
        function questionSet(qnum){
          $(".btns").off("click");
          $(".btns").removeClass("activ abut").addClass("abut");
          $("#btnconfirm").removeClass("abut").addClass("dab");
          if (qnum == der.length){
            // out of range handler
          } else {
            var trueNum = rlist[qnum];
            var qobj = der[trueNum];
            $("#question_container").text(qobj[1]);
            var currSel = [undefined];
            btns[qnum].map((btns, shuf) => {$("#btn"+btns).text(qobj[shuf+2]).click(() => {selection(btns); currSel[0] = btns;});});
            $("#btnconfirm").text("Confirm!").click(() => {
              if (currSel[0]){
                console.log(currSel[0]);
                $("#btnconfirm").text((qnum + 1 == der.length)?"Finish!":"Continue!");
                $(".btns").off("click").removeClass("abut");
                $("#btnconfirm").click(() => {questionSet(qnum + 1)}).addClass("abut");
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
            console.log(CryptoJs.enc.Hex.stringify(dec));
            try {
              var der = JSON.parse(CryptoJs.enc.Utf8.stringify(dec));
              console.log(der);
              setTimeout(pQuestion, 0, der);
            } catch (error){
              dFR--;
              console.log(error);
              if (dFR > 0){
                console.log("Retry:", dFR);
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