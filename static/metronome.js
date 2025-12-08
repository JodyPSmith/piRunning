let audioFile = "metronome.mp3";
let freqnecy = 160; // default frequency
let metronome = false

const metronomeToggle = async () => {
    console.log("Metronome Toggle pressed");
    metronome = !metronome
    if (metronome) {
        playMetronome()
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

const playMetronome = () => {
    if (metronome) {
        let audio = new Audio(audioFile);
        // play the audio frequency times per minute
        audio.play();
        setTimeout(playMetronome, 60000 / freqnecy);
    }
}
