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

const startRun = async () => {
  console.log("Start Run pressed");
  ws.send(JSON.stringify({
    type: "start",
    value: 1
  }))
}

const stopRun = async () => {
  console.log("Stop Run pressed");
  ws.send(JSON.stringify({
    type: "stop",
    value: 1
  }))
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
  speed.innerHTML = data.speed.toFixed(1) 
  incline.innerHTML = data.incline.toFixed(1)
};

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

const convertSpeedOrDistance = (distanceKm) => {
  if (config.unitsDistance === "metric") {
    return distanceKm;
  } else {
    return distanceKm * 0.621371; // Convert km to miles
  }
}

const convertWeight = (weightKg) => {
  if (config.unitsWeight === "metric") {
    return weightKg;
  } else {
    return weightKg * 2.20462; // Convert kg to pounds
  }
}
