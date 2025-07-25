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


const button_change = document.querySelector(".btn-change")

button_change.addEventListener("click", () => {
    let new_h4 = document.querySelector(".txt-changed")
    new_h4.textContent = "Has cambiado el H3 por este texto!"
})

let colores = ["yellow" , "blue", "red"]
let colorIndex = 0


// Añadiendo un div para cambiarle el color mediante un array

const container = document.createElement("div")
container.style.backgroundColor = "#86cf9a"
container.style.width = "200px"
container.style.height = "100px"
container.style.borderRadius = "20px"

const div_title = document.createElement("h3")
div_title.textContent = "Changing my color"

div_title.style.textAlign = "Center"


const button_change_color = document.createElement("button")
button_change_color.textContent = "Cambiar color"


container.style.display = "flex"
container.style.flexDirection = "column" // Para que el h3 y el boton este uno debajo del otro
container.style.alignContent = "center" // centramos horizontalmente los hijos (h3 y el boton)

button_change_color.addEventListener("click", () => {
    container.style.backgroundColor = colores[colorIndex]
    colorIndex = (colorIndex + 1) % colores.length // Hacemos una operacion de modulo para que cuando llegue al ultimo indice se repita nuevamente

})

container.appendChild(div_title)
container.appendChild(button_change_color)




document.body.appendChild(container)
