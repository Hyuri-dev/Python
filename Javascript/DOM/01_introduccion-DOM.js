let title = document.getElementById("h1");

console.log(title);

const paragraph = document.querySelector("p")
paragraph.style.color = "green"

const button_event = document.querySelector("#btn")

button_event.addEventListener("click", () => {

    let mensaje = document.createElement("h3")
    mensaje.textContent = "Has interactuado con el boton y has liberado este mensaje!"
    document.body.appendChild(mensaje)
})