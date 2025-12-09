let audioFile = "metronome.mp3";
let freqnecy = 160; // default frequency
let metronome = false

const metronomeToggle = async () => {
    console.log("Metronome Toggle pressed");
    let metronomeButton = document.getElementById("metronomeToggle")
    metronome = !metronome
    if (metronome) {
        playMetronome()
        metronomeButton.innerHTML = "Metronome: On"
        metronomeButton.style.backgroundColor = "rgb(34, 177, 76)";
    } else {
        metronomeButton.innerHTML = "Metronome: Off"
        metronomeButton.style.backgroundColor = "rgb(72, 122, 216)";
    }
}
const metronomeSet = async (value) => {
    let metronomeDisplay = document.getElementById("metronome")
    if (value === "increase") {
        freqnecy += 5
        metronomeDisplay.innerHTML = freqnecy
    } else if (value === "decrease") {
        freqnecy -= 5
        metronomeDisplay.innerHTML = freqnecy
    }
}

const metronomeText = document.getElementById("metronome")
const playMetronome = () => {
    if (metronome) {
        let audio = new Audio(audioFile);
        // play the audio frequency times per minute
        audio.play();
        setTimeout(playMetronome, 60000 / freqnecy);
        pulseText();
    }
}
const pulseText = () => {
    if (metronome) {
        metronomeText.style.fontSize = "30px";
        setTimeout(() => {
            metronomeText.style.fontSize = "25px";
        }, 60000 / freqnecy / 2);
    }
}