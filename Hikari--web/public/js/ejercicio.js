console.log("JS cargado correctamente");
const habilidades = {
    alta: {  // Nivel 8–10
        nombre: "TIP: cambiar la activación del cuerpo",
        descripcion: "Habilidades breves basadas en el cuerpo para bajar de forma rápida la intensidad emocional.",
        ejercicios: [
            {
                nombre: "Respiración rápida y después profunda",
                pasos: [
                    "Si tu nivel de malestar es muy alto, siéntate con seguridad.",
                    "Inhala y exhala más rápido de lo normal durante unos segundos.",
                    "Luego cambia intencionalmente a respiración lenta y profunda.",
                    "Mantén el ritmo lento durante un minuto.",
                    "Evalúa tu nivel de malestar después."
                ]
            },
            {
                nombre: "Cambio de temperatura en manos o rostro",
                pasos: [
                    "Llena un recipiente con agua fresca o usa una toalla húmeda.",
                    "Apoya tus manos o rostro en el agua por unos segundos.",
                    "Respira calmadamente mientras sientes la temperatura.",
                    "Repite varias veces si no hay contraindicaciones médicas.",
                    "Nota cualquier cambio en la emoción."
                ]
            }
        ]
    },

    media: { // Nivel 4–8
        ejercicios: [
            {
                nombre: "Cálmate con los cinco sentidos",
                pasos: [
                    "Observa tres cosas que puedas ver.",
                    "Escucha tres sonidos distintos.",
                    "Identifica un olor en el ambiente.",
                    "Toma un sorbo de algo o imagina un sabor agradable.",
                    "Toca dos superficies y describe su textura.",
                    "Evalúa el malestar al terminar."
                ]
            }
        ]
    }
};


// Recuperamos nivel
const nivel = parseInt(localStorage.getItem("nivelMalestar"));
let ejercicioActual = 0;
let habilidadSeleccionada;

// Selección de habilidad según nivel
if (nivel >= 8) {
    habilidadSeleccionada = habilidades.alta;
} else {
    habilidadSeleccionada = habilidades.media;
}

const titulo = document.getElementById("titulo-habilidad");
const descripcion = document.getElementById("descripcion-habilidad");
const lista = document.getElementById("lista-pasos");
const btnSiguiente = document.getElementById("btnSiguiente");

// Cargar el ejercicio actual
function cargarEjercicio() {
    const ejercicio = habilidadSeleccionada.ejercicios[ejercicioActual];
    
    titulo.textContent = ejercicio.nombre;
    descripcion.textContent = habilidadSeleccionada.descripcion;
    lista.innerHTML = "";

    ejercicio.pasos.forEach((paso, i) => {
        const li = document.createElement("li");

        const check = document.createElement("input");
        check.type = "checkbox";
        check.classList.add("checkbox-paso");
        check.dataset.index = i;

        check.addEventListener("change", verificarPasos);

        li.appendChild(check);
        li.appendChild(document.createTextNode(paso));
        lista.appendChild(li);
    });
}

function verificarPasos() {
    const checks = document.querySelectorAll(".checkbox-paso");
    const todosMarcados = [...checks].every(ch => ch.checked);

    btnSiguiente.disabled = !todosMarcados;
}

btnSiguiente.addEventListener("click", () => {
    localStorage.setItem("nivelMalestar", nivel);
    localStorage.setItem("ejercicioActual", ejercicioActual);

    window.location.href = "evaluacion.html";
});

cargarEjercicio();
