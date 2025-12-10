
const habilidades = {
    alta: {  // Nivel 8–10
        descripcion: "Habilidades breves basadas en el cuerpo para bajar la intensidad emocional.",
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
                    "Nota cualquier cambio en la intensidad emocional."
                ]
            }
        ]
    },

    media: { // Nivel 4–8
        descripcion: "Usar los sentidos para recuperar calma y seguridad.",
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


let nivel = parseInt(localStorage.getItem("nivelMalestar"));
let ejercicioActual = parseInt(localStorage.getItem("ejercicioActual"));

if (isNaN(ejercicioActual)) ejercicioActual = 0; // evita errores


let habilidadSeleccionada = nivel >= 8 ? habilidades.alta : habilidades.media;


const titulo = document.getElementById("titulo-habilidad");
const descripcion = document.getElementById("descripcion-habilidad");
const lista = document.getElementById("lista-pasos");
const btnSiguiente = document.getElementById("btnSiguiente");


function cargarEjercicio() {
    const ejercicio = habilidadSeleccionada.ejercicios[ejercicioActual];

    // En caso de que alguien avance más de lo permitido
    if (!ejercicio) {
        ejercicioActual = 0;
        localStorage.setItem("ejercicioActual", 0);
    }

    titulo.textContent = ejercicio.nombre;
    descripcion.textContent = habilidadSeleccionada.descripcion;

    lista.innerHTML = "";

    ejercicio.pasos.forEach((paso, index) => {
        const li = document.createElement("li");

        const check = document.createElement("input");
        check.type = "checkbox";
        check.classList.add("checkbox-paso");
        check.dataset.index = index;

        check.addEventListener("change", verificarPasos);

        li.appendChild(check);
        li.appendChild(document.createTextNode(paso));
        lista.appendChild(li);
    });

    btnSiguiente.disabled = true;
}


function verificarPasos() {
    const checks = document.querySelectorAll(".checkbox-paso");
    const completos = [...checks].every(c => c.checked);
    btnSiguiente.disabled = !completos;
}


btnSiguiente.addEventListener("click", () => {
    localStorage.setItem("nivelMalestar", nivel);
    localStorage.setItem("ejercicioActual", ejercicioActual);
    window.location.href = "evaluacion.html";
});


cargarEjercicio();
