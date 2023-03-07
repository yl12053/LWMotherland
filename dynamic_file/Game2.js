((px, py, hx) => {
  var ableExit = true;
  $(window).on("beforeunload", function(e){
    if (!ableExit){
      e.preventDefault();
      return false;
    }
  });
  var AC = {
    'flag': false,
    'audio_file': new Audio(assets_url + "/audio/AC/angus.mkv"),
    'start_func': function(){
      ableExit = false;
      this.flag = true;
      var temp = this;
      function g(){
        function p(){
          var audio = temp.audio_file;
          audio.play();
          audio.onended = function(){
            audio.currentTime = 0;
            setTimeout(p, 0);
          };
        }
        if (!ActiveQ()){
          if (temp.flag){
            setTimeout(p, 0);
            setInterval(() => {alert("AC");})
          }
        }
        if (temp.flag){
          setTimeout(g, 0);
        }
      }
      setTimeout(g, 0);
    },
    'end_func': function(){
      ableExit = true;
      this.flag = false;
    }
  }
  function giveR(){
    if ($("#btnright").length){
      $("#btnright").click(function (){
        AC.end_func();
        window.location = "/map";
      });
    } else {
      setTimeout(giveR, 0);
    }
  }
  setTimeout(giveR, 0);
  //{% raw %}
  function escape(text){
    var elem = document.createElement('textarea');
    elem.textContent = text;
    return elem.innerHTML;
  }
  setInterval(() => {
    $.ajax({
      "url": "/apis/game2/keep_key_alive",
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
    "url": "/apis/game2/ecdhe",
    "method": "POST",
    "data": {
      "hx": hx,
      "px": String(pointx),
      "py": String(pointy)
    }
  }).then(data => {
    var shared = (new nobleSecp256k1.Point(px, py)).multiply(BigInt("0x"+nobleSecp256k1.utils.bytesToHex(privkey)));
    var shared_key = new BN(shared.x).toString(16).padStart(64, '0');
    var shared_iv = new BN(shared.y).toString(16).padStart(64, '0').slice(0, 32);
    return new Promise((resolve, reject) => $.ajax({
      "url": "/apis/game2/fetch",
      "method": "POST",
      "data": {"hx": hx}
    }).then(data => resolve([data, shared_key, shared_iv]), data => reject([data, shared_key, shared_iv])));
  }).then((data) => {
    var key = data[1];
    var iv = data[2];
    var data = data[0];
    var ivd = CryptoJs.enc.Hex.parse(iv);
    var dec = CryptoJs.AES.decrypt(data, CryptoJs.enc.Hex.parse(key), { iv: ivd });
    var dec_json = JSON.parse(CryptoJs.enc.Utf8.stringify(dec));
    var ivdBuffer = CryptoJs.SHA256(ivd);
    var ivdHex = CryptoJs.enc.Hex.stringify(ivdBuffer).slice(0, 32);
    var ivdFinal = CryptoJs.enc.Hex.parse(ivdHex);
    dec_json.sort(function(a, b){return a[0]-b[0];});
    var totht = "";
    var answer_storage = {};
    var answer_handin = [];
    var mapA2C = window.localStorage.getItem("P^=p+PKZ*D9U}=i#");
    if (mapA2C == null || JSON.parse(mapA2C).length != dec_json.length){
      var fCac = [...Array(dec_json.length).keys()];
      fCac.sort(() => Math.random() - 0.5);
      window.localStorage.setItem("P^=p+PKZ*D9U}=i#", JSON.stringify(fCac));
    } else {
      fCac = JSON.parse(mapA2C);
    }
    console.log(dec_json);
    // dec_json.sort((d1, d2) => fCac[d1[0]-1] - fCac[d2[0]-1]);
    dec_new_json = [];
    for (var n of fCac){
      dec_new_json.push(dec_json[n]);
    }
    dec_json = dec_new_json;
    console.log(dec_json);
    var noq = 0;
    for (var x of dec_json){
      noq++;
      var html = `<br><br>${noq}.  `;
      var replace_obj = {};
      var answer_temp = [];
      for (var y = 1; y <= x[3].length; y++){
        var replace_regex = "{{ +replace_" + y + " *\\| *safe *}}";
        var replace_content = `<span class='blank'><span class='text_container' id='q${noq}_${y}'>&nbsp;</span><span style='display: none' class='choice_cloud'>`;
        answer_storage[`${noq}_${y}`] = -1;
        answer_temp[y-1] = -1;
        for (var i = 0; i < x[2][y-1].length; i++){
          replace_content = replace_content + `<span attrs='${noq}_${y}_${i}' class='choice'>${escape(x[2][y-1][i])}</span>`;
        }
        replace_content = replace_content + "</span></span>";
        replace_obj[replace_regex] = replace_content;
      }
      answer_handin[x[0]-1] = answer_temp;
      var toBe = x[1];
      for (var reg in replace_obj){
        toBe = toBe.replace(new RegExp(reg), replace_obj[reg]);
      }
      html += toBe + "<br><hr></hr>";
      totht += html;
    }
    console.log(answer_handin);
    $("#wrapper")[0].innerHTML = totht;
    var all_choices = $(".blank")
      .parent()
      .find(".choice_cloud");
    
    $(".content_container").on("click", ".blank", function() {
      event.stopPropagation(); // Prevent the 'clicking anywhere hides it' function
      all_choices.hide("slow");
      var choiceCloud = $(this).find(".choice_cloud");
      choiceCloud.toggle();
      Array.from($(".choice_cloud")).forEach((elem) => {$(elem).css("width", ($(".content_container")[0].getBoundingClientRect().width + $(".content_container")[0].getBoundingClientRect().x - elem.getBoundingClientRect().x) + "px");});
    });
    $(".choice").click(function(event) {
      var myChoice = $(event.target);
      var isChoice = myChoice.is(".choice");
      event.stopPropagation(); // Prevent the 'clicking anywhere hides it' function
      if (isChoice) {
        //make sure I am a .choice element
        myChoice.closest(".blank")
          .find(".text_container")
          .text(myChoice.text());
        myChoice.parent().hide();
        var attrs = myChoice.attr("attrs");
        console.log(attrs);
        var sol = splitOnlast(attrs, "_")[0];
        var ql = sol.split("_");
        var choice = splitOnlast(attrs, "_")[1];
        answer_storage[sol] = Number(choice);
        var reverseSearch = JSON.parse(window.localStorage.getItem("P^=p+PKZ*D9U}=i#"));
        console.log(reverseSearch);
        // reverseSearch = [...Array(reverseSearch.length).keys()].map((v) => reverseSearch.indexOf(v));
        // console.log(reverseSearch);
        console.log(ql);
        console.log(answer_handin);
        answer_handin[dec_json[Number(ql[0])-1][0]-1][Number(ql[1])-1] = Number(choice);
      }
    });
    
    // Clicking anywhere else hides it
    $(document).on("click", function() {
      $(".choice_cloud").hide("slow");
    });
    $("#btnleft").click(() => {
      var count = 0;
      var correct = 0;
      all_choices.hide("slow");
      $(".content_container").off("click");
      for (var x in answer_storage){
        var qnum = Number(x.split("_")[0])-1;
        var cnum = Number(x.split("_")[1])-1;
        var sele = answer_storage[x];
        if (sele == dec_json[qnum][3][cnum]){
          $("#q"+x).parent().css("background-color", "lightgreen").css("color", "rgb(7, 165, 22)");
          correct++;
        } else {
          $("#q"+x).parent().css("background-color", "lightpink").css("color", "rgb(165, 7, 22)");
        }
        count++;
      }
      var handin_str = JSON.stringify(answer_handin);
      console.log(handin_str);
      var res = CryptoJs.AES.encrypt(handin_str, CryptoJs.enc.Hex.parse(key), { iv: ivdFinal });
      var base = CryptoJs.enc.Base64.stringify(res.ciphertext);
      $.ajax({
        "url": "/apis/game2/hand_in",
        "method": "POST",
        "data": {
          "hx": hx,
          "raw": base
        },
      }).then((res) => {
        AC.end_func();
      }, (res) => {AC.end_func();});
    });
    // AC.start_func();
  });
  //{% endraw %}
})(BigInt("{{ px }}"), BigInt("{{ py }}"), "{{ hx }}");