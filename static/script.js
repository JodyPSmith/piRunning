console.log("Server is running...");
console.log("Your config is", config)
const ws = new WebSocket(`ws://${config.serverIP}:${config.port}/ws`);

const inclineSet = async (value) => {
  console.log("Incline Set pressed");
  ws.send(JSON.stringify({
    type: "inclineSet",
    value: value
  }))
}

const speedSet = async (value) => {
  console.log("Speed Set pressed");
  ws.send(JSON.stringify({
    type: "speedSet",
    value: value
  }))
}

let intervalId;
const startRun = async () => {
  console.log("Start Run pressed");
  if (!intervalId) { // Prevent multiple intervals from starting
    intervalId = setInterval(syncData, 1000); // Start the function every second
    ws.send(JSON.stringify({
      type: "start",
      value: 1
    }))
  }

}

const stopRun = async () => {
  console.log("Stop Run pressed");
  if (intervalId) {
    clearInterval(intervalId); // Stop the interval
    intervalId = null; // Reset the ID
    ws.send(JSON.stringify({
      type: "stop",
      value: 1
    }))
  }
}

// this is what it does when it gets a message
ws.onmessage = function (event) {
  console.log(event.data);
  let data = JSON.parse(event.data)
  console.log("Parsed data:", data)
  let distance = document.getElementById("distance")
  let heartrate = document.getElementById("heartrate")
  let calories = document.getElementById("calories")
  let duration = document.getElementById("duration")
  let incline = document.getElementById("incline")
  let speed = document.getElementById("speed")

  distance.innerHTML = data.distance.toFixed(2) + ` ${config.unitsDistance}/h`
  heartrate.innerHTML = data.heart_rate.toFixed(0) + ` bpm`
  calories.innerHTML = data.calories.toFixed(0) + ` kcal`
  duration.innerHTML = formatSecondsToHHMMSS(data.duration_seconds)
  speed.innerHTML = convertSpeedOrDistance((data.speed * 10)).toFixed(2)
  incline.innerHTML = data.incline.toFixed(1)
};

const syncData = async () => {
  ws.send(JSON.stringify({
    type: "sync",
    value: 1
  }))
}

const formatSecondsToHHMMSS = (totalSeconds) => {
  const hours = Math.floor(totalSeconds / 3600);
  totalSeconds %= 3600; // Get the remaining seconds after extracting hours
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  // Pad single-digit numbers with a leading zero
  const formattedHours = String(hours).padStart(2, '0');
  const formattedMinutes = String(minutes).padStart(2, '0');
  const formattedSeconds = String(seconds).padStart(2, '0');

  return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
}

// T6.5 Si machine reports in mph
const convertSpeedOrDistance = (distance) => {
  if (config.unitsDistance === "km") {
    console.log("Converting to km");
    return distance * 1.60934;
  } else {
    return distance
  }
}

const convertWeight = (weightKg) => {
  if (config.unitsWeight === "metric") {
    return weightKg;
  } else {
    return weightKg * 2.20462; // Convert kg to pounds
  }
}
