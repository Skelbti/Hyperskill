document.addEventListener("keydown", function(event) {
    let evt = ["KeyA", "KeyS", "KeyD", "KeyF", "KeyG", "KeyH", "KeyJ", "KeyW", "KeyE", "KeyT", "KeyY", "KeyU"];
    let input = event.code;

    if (evt.includes(input)){
        let audio = new Audio("sound/" + input.slice(3,5) + ".mp3");
        audio.play();
    } else {
        console.log("WARNING : Unbound key was pressed!");
    }
});
