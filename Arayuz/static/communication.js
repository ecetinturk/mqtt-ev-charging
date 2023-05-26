var socket = io();
var carContainers = document.getElementsByClassName('container');
var messages = document.getElementsByClassName('message');
var previousChargeLevels = {}; // Store previous charge levels for each car
previousChargeLevels['v_0'] = 1000;  // Store previous charge level for car v_0
previousChargeLevels['v_1'] = 1000;  // Store previous charge level for car v_1
previousChargeLevels['v_2'] = 1000;
previousChargeLevels['v_3'] = 1000;
previousChargeLevels['v_4'] = 1000;



socket.on('mqtt_message', function (message) {
    const colonIndex = message.indexOf(":");
    const substringAfterColon = message.substring(colonIndex + 1);
    const trimmedString = substringAfterColon.trim();
    const parts = trimmedString.split(" ");
    var carId = parts[0];
    var chargeLevel = parts[1];
    var routeInfo = parts[2];
    var chargeStation = parts[3];
    // var chargeLevel = message.substring(message.indexOf(':') + 1, message.indexOf('r')).trim();
    // var routeInfo = message.substring(message.indexOf('r')).trim();

    // Find the car container based on car ID
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

    if (carContainer) {
        // Find the elements within the car container
        var messageElement = carContainer.querySelector('.message');
        var carIdElement = carContainer.querySelector('.car-id');
        var chargeLevelElement = carContainer.querySelector('.charge-level');
        var routeInfoElement = carContainer.querySelector('.route-info');
        var chargeStationElement = carContainer.querySelector('.charge-station');

        // Update the values
        messageElement.innerHTML = message;
        carIdElement.innerHTML = 'Car ID: ' + carId;
        chargeLevelElement.innerHTML = 'Charge Level: ' + chargeLevel;
        routeInfoElement.innerHTML = 'Route: ' + routeInfo;
        chargeStationElement.innerHTML = 'Charge Station: ' + chargeStation;
    }
    var previousChargeLevel = previousChargeLevels[carId];
    if (previousChargeLevel !== undefined) {
        if (chargeLevel == 1000) {
            carContainer.classList.remove('container-red', 'container-green');
            carContainer.classList.add('container-orange');
            messageElement.innerHTML = 'Full Battery: ' + chargeLevel;
        } else if (chargeLevel < previousChargeLevel) {
            carContainer.classList.remove('container-green', 'container-orange');
            carContainer.classList.add('container-red');
            messageElement.innerHTML = 'Discharging: ' + chargeLevel;
        } else if (chargeLevel > previousChargeLevel) {
            carContainer.classList.remove('container-red', 'container-orange');
            carContainer.classList.add('container-green');
            messageElement.innerHTML = 'Charging: ' + chargeLevel; 
        }
        else {
            // Initial state, show the current charge level
            messageElement.innerHTML = 'Charging: ' + chargeLevel;
        }
    }
    

    // Store the current charge level as the previous charge level for the car
    previousChargeLevels[carId] = chargeLevel;
}
);