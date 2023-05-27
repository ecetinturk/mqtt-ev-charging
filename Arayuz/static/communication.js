var socket = io();
var carContainers = document.getElementsByClassName('container');
var messages = document.getElementsByClassName('message');
var previousChargeLevels = {};       // Her aracın ilk şarjının saklanacağı değişken
previousChargeLevels['v_0'] = 1000;  // v_0 aracının ilk şarjı
previousChargeLevels['v_1'] = 1000;  // v_1 aracının ilk şarjı
previousChargeLevels['v_2'] = 1000;  // v_2 aracının ilk şarjı
previousChargeLevels['v_3'] = 1000;  // v_3 aracının ilk şarjı
previousChargeLevels['v_4'] = 1000;  // v_4 aracının ilk şarjı

socket.on('mqtt_message', function (message) {
  //MQTT aracılığıyla gelen mesajın parse edilerek ilgili değişkenlere atandığı kısım//
  const colonIndex = message.indexOf(":");
  const substringAfterColon = message.substring(colonIndex + 1);
  const trimmedString = substringAfterColon.trim();
  const parts = trimmedString.split(" ");
  var carId = parts[0];
  var chargeLevel = parts[1];
  var routeInfo = parts[2];
  var chargeStation = parts[3];

// Araç id^Sine göre araç konteynerini bul
  var carContainer;
  if (carId === 'v_0') {
    carContainer = document.getElementById('container1');
  } else if (carId === 'v_1') {
    carContainer = document.getElementById('container2');
  } else if (carId === 'v_2') {
    carContainer = document.getElementById('container3');
  }
  else if (carId === 'v_3') {
    carContainer = document.getElementById('container4');
  }
  else if (carId === 'v_4') {
    carContainer = document.getElementById('container5');
  }
  else {
    carContainer = null;
  }
  if (carContainer) { // Arabalara atanan containerlara içindeki öğeleri bulun
    var messageElement = carContainer.querySelector('.message');
    var carIdElement = carContainer.querySelector('.car-id');
    var chargeLevelElement = carContainer.querySelector('.charge-level');
    var routeInfoElement = carContainer.querySelector('.route-info');
    var chargeStationElement = carContainer.querySelector('.charge-station');
    var charge_percent = Math.round(chargeLevel / 10);
    //Verilerin Güncellenmesi
    messageElement.innerHTML = message;
    carIdElement.innerHTML = 'Car ID: ' + carId;
    chargeLevelElement.innerHTML = 'Charge Level: ' + charge_percent + '%';
    routeInfoElement.innerHTML = 'Route: ' + routeInfo;
    chargeStationElement.innerHTML = 'Charge Station: ' + chargeStation;
  }


  var previousChargeLevel = previousChargeLevels[carId];
  if (previousChargeLevel !== undefined) {
    if (chargeLevel > previousChargeLevel) {
      carContainer.classList.remove('container-red', 'container-orange');
      carContainer.classList.add('container-green');
      messageElement.innerHTML = 'Charging: ' + (chargeLevel / 10).toFixed(3) + 'kW';
    } else if (chargeLevel < previousChargeLevel) {
      carContainer.classList.remove('container-green', 'container-orange');
      carContainer.classList.add('container-red');
      messageElement.innerHTML = 'Discharging: ' + (chargeLevel / 10).toFixed(3) + 'kW';
    }
    else {
      // İlk durum, mevcut şarj seviyesini gösterir
      messageElement.innerHTML = 'Charging: ' + (chargeLevel / 10).toFixed(3) + 'kW';
    }
  }

  // Şarjın 1000,00'e eşit olup olmadığını kontrol edilir
  if (chargeLevel == 1000.00) {
    carContainer.classList.remove('container-red', 'container-green');
    carContainer.classList.add('container-orange');
    messageElement.innerHTML = 'Full Battery: ' + (chargeLevel / 10).toFixed(3) + 'kW';
  }
  // Mevcut şarj seviyesini araç için önceki şarj seviyesi olarak kaydetme
  previousChargeLevels[carId] = chargeLevel;
});