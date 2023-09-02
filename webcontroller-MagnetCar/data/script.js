/*setInterval(function () {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            carP.innerHTML = direction[obj.dir - 1].value;
            powP.innerHTML = obj.pwm;
            mode.checked = obj.mode;
            if (obj.mode == 1 ) {
                modeP.innerHTML = "Auto";
                mode.checked = true
            }
            else {
                modeP.innerHTML = "Manual";
                mode.checked = false;
            }

        }
    };
    xhttp.open("GET", "/state", true);
    xhttp.send();
},2000);*/

if (!!window.EventSource) {
  var source = new EventSource('/events');

  source.addEventListener('open', function (e) {
    console.log("Events Connected");
  }, false);

  source.addEventListener('error', function (e) {
    if (e.target.readyState != EventSource.OPEN) {
      console.log("Events Disconnected");
    }
  }, false);

  source.addEventListener('data_readings', function (e) {
    console.log("data_readings", e.data);
    var obj = JSON.parse(e.data);
    carP.innerHTML = direction[obj.dir - 1].value;
    powP.innerHTML = obj.pwm;
    lenP.innerHTML = obj.len

  }, false);

}

var direction = document.getElementsByClassName("direction");
var carP = document.getElementById("carPos");
carP.innerHTML = direction[4].value; //顯示預設的值 Stop
car = direction[4].name;
for (var i = 0; i < direction.length; i++) {
  direction[i].onclick = function () {
    carP.innerHTML = this.value;
    car = this.name;
    value("dir", car);
  }
}

var Value = document.getElementById("powvalue");
var powP = document.getElementById("powPos");
powP.innerHTML = Value.value; //顯示預設的值 會顯示中間值
Value.oninput = function () {
  Value.value = this.value;
  powP.innerHTML = this.value;
  delayShowData("pwm", Value.value);
  // console.log(Value.value)
}

var lenAngle = document.getElementById("lenAngle")
var lenP = document.getElementById("lenPos");
powP.innerHTML = lenAngle.value; //顯示預設的值 會顯示中間值
lenAngle.oninput = function () {
  lenAngle.value = this.value;
  lenP.innerHTML = this.value;
  delayShowData("len", lenAngle.value);
  // console.log(Value.value)
}


var timers = {};
function delayShowData(type, values) {
  clearTimeout(timers[type]);
  timers[type] = setTimeout(function () {
    $('span.' + type).text(values[0] + 'mm - ' + values[1] + 'mm');
    value(type, values);
  }, 300);
}
$.ajaxSetup({ timeout: 1000 });
function value(type, pos) {
  $.get("/?" + type + "=" + pos + "&");
  { Connection: close };
}

