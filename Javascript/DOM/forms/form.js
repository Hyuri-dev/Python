/* Podemos llamar un formulario html por element id, por su indice tomando en cuenta la posicion en que esta, por nombre si se le atribuye un nombre al formulario */

// Formas de acceder con element: 

const form = document.getElementById('form')

//  Forma de acceder con document: 

//  Por su posicion (indice)
const firstFrom = document.forms[0] // accediendo al primer formulario creado de la pagina

// Por nombre

const myForm = document.forms['formName']

// Por ID 

const myNameForm = document.forms['formId']




//Accediendo a los datos del formulario 

const formulario = document.getElementById("formulario")
const errorMessage  = document.querySelector(".error-message")

// Es posible ingresar a los datos del formulario con form.elements y con el nombre que se le haya ingresado al campo que queremos obtener o por su indice
formulario.addEventListener("submit", function (event){
    event.preventDefault()

    const {usuario , contraseña} = formulario.elements

    errorMessage.innerHTML = ""

    if(!usuario.value.trim()) { // usamos .trim para eliminar los espacios en blanco
        displayError("usuario is required")
        return
    }

    if (!contraseña.value.trim() || !isStrongPassword(contraseña.value)) {
        displayError("Wrong or error password")
        return
    }
    alert("Registro exitoso!")
})

function displayError(message) {
    errorMessage.innerHTML += `<div class="error-message">${message}</div>`;
}

function isStrongPassword(contraseña) {
    return /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/.test(contraseña);
}

// Segundo formulario 

const formularioSuma = document.getElementById("myForm2")
const resultado = document.querySelector(".resultado")
const listado = document.getElementById("selector")

// console.log (listado.textContent)

formularioSuma.addEventListener("submit", function(event){
    event.preventDefault()

    const valor1 = document.getElementById("entryValor1").value
    const valor2 = document.getElementById("entryValor2").value


    const tituloResultado = document.createElement("h4")
    // tituloResultado.textContent = `el resultado es: ${String(suma)}`

    // const seleccion = listado.selectedIndex
    // const opciones = listado.options[seleccion]
    const opciones = listado.value

    switch (Number(opciones)) {
        case 1 :
            const suma = Number(valor1) + Number(valor2)
            tituloResultado.textContent = `el resultado es: ${String(suma)}`
            break
        case 2:
            const resta = Number(valor1) - Number(valor2)
            tituloResultado.textContent = `el resultado es: ${String(resta)}`
            break
        case 3:
            const multiplicacion = Number(valor1) * Number(valor2)
            tituloResultado.textContent = `el resultado es: ${String(multiplicacion)}`
            break
        case 4: 
            const division = Number(valor1) / Number(valor2)
            tituloResultado.textContent = `el resultado es: ${String(division)}`

        
    }


// Los valores obtenidos de los inputs vienen de tipo texto, por lo tanto hay que pasarlos a enteros 


    resultado.innerHTML=""
    resultado.appendChild(tituloResultado)

})
