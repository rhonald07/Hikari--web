console.log("Nivel recibido:", localStorage.getItem("nivelMalestar"));

document.addEventListener("DOMContentLoaded", () => {

    const titulo = document.getElementById("titulo-habilidad");
    const descripcion = document.getElementById("descripcion-habilidad");
    const lista = document.getElementById("lista-pasos");
    const btnSiguiente = document.getElementById("btnSiguiente");

    if (!titulo || !descripcion || !lista || !btnSiguiente) {
        console.error("Faltan elementos en el HTML de ejercicio");
        return;
    }

    const urlContactos = "/contactos-emergencia/";

    // ======= RECUPERAR NIVEL =======
    let nivel = parseInt(localStorage.getItem("nivelMalestar") || "5", 10);
    console.log("Nivel desde localStorage:", nivel);

    // ======= HABILIDADES =======
    const habilidades = {

        media: {
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
        },

        alta: {
            descripcion: "Habilidades basadas en el cuerpo para bajar la intensidad emocional.",
            ejercicios: [
                {
                    nombre: "Respiración rápida y después profunda",
                    pasos: [
                        "Si tu nivel de malestar es muy alto, siéntate con seguridad.",
                        "Inhala y exhala más rápido de lo normal durante unos segundos.",
                        "Luego cambia intencionalmente a respiración lenta y profunda.",
                        "Mantén el ritmo lento durante un minuto.",
                        "Evalúa tu intensidad emocional después."
                    ]
                },
                {
                    nombre: "Cambio de temperatura en manos o rostro",
                    pasos: [
                        "Llena un recipiente con agua fresca o usa una toalla húmeda.",
                        "Apoya tus manos o rostro en el agua por unos segundos.",
                        "Respira calmadamente mientras sientes la temperatura.",
                        "Repite varias veces si no hay contraindicaciones médicas.",
                        "Nota cualquier cambio en tu nivel emocional."
                    ]
                }
            ]
        }
    };

    // ======= SECUENCIA DE EJERCICIOS =======
    let secuencia = [];
    let descripcionTexto = "";

    if (nivel < 8) {
        console.log("Flujo: media → alta");
        secuencia = [
            ...habilidades.media.ejercicios,
            ...habilidades.alta.ejercicios
        ];
        descripcionTexto = habilidades.media.descripcion;

    } else {
        console.log("Flujo solo alta");
        secuencia = [...habilidades.alta.ejercicios];
        descripcionTexto = habilidades.alta.descripcion;
    }

    descripcion.textContent = descripcionTexto;

    let ejercicioActual = 0;
    let habilidadesUsadas = [];

    cargarEjercicio();

    // ======= CARGAR EJERCICIO =======
    function cargarEjercicio() {

        const ejercicio = secuencia[ejercicioActual];

        if (!ejercicio) {
            console.log("No hay más ejercicios → guardando historial");
            guardarHistorial();
            return;
        }

        titulo.textContent = ejercicio.nombre;
        lista.innerHTML = "";
        btnSiguiente.disabled = true;

        ejercicio.pasos.forEach((paso, index) => {
            const li = document.createElement("li");

            const check = document.createElement("input");
            check.type = "checkbox";
            check.classList.add("checkbox-paso");

            check.addEventListener("change", verificarPasos);

            li.appendChild(check);
            li.appendChild(document.createTextNode(paso));
            lista.appendChild(li);
        });

        habilidadesUsadas.push(ejercicio.nombre);
    }

    // ======= VERIFICAR PASOS =======
    function verificarPasos() {
        const checks = document.querySelectorAll(".checkbox-paso");
        const completos = [...checks].every(c => c.checked);
        btnSiguiente.disabled = !completos;
    }

    // ======= SIGUIENTE =======
    btnSiguiente.addEventListener("click", () => {
        ejercicioActual++;

        if (ejercicioActual >= secuencia.length) {
            guardarHistorial();
        } else {
            cargarEjercicio();
        }
    });

    // ======= GUARDAR HISTORIAL EN DJANGO =======
    function guardarHistorial() {

        fetch("/guardar-nivel/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                nivel: nivel,
                habilidades: habilidadesUsadas
            })
        })
        .then(() => {
            console.log("Historial guardado");
            window.location.href = urlContactos;
        })
        .catch(err => console.error("Error enviando historial:", err));
    }

    // CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie) {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = cookie.substring(name.length + 1);
                    break;
                }
            }
        }
        return cookieValue;
    }

});
