document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById("sliderMalestar");
    const nivelText = document.getElementById("nivelText");
    const nivelBox = document.getElementById("nivelBox");
    const emojis = document.querySelectorAll("#emojiLine .emoji");
    const emojiLine = document.getElementById("emojiLine");
    const btnContinuar = document.getElementById("btnContinuar");

    if (!slider || !nivelText || !nivelBox || !btnContinuar) {
        console.error("Faltan elementos en el HTML de crisis");
        return;
    }

    let nivelActual = 1;

    const colores = [
        "#2ecc71", "#55d86c", "#7fe067", "#a8e862", "#d1f05d",
        "#f1c40f", "#e67e22", "#d35400", "#c0392b", "#96281b"
    ];

    function actualizarUI() {
        const idx = Math.min(Math.max(Math.round(slider.value) - 1, 0), 9);
        nivelActual = idx + 1;

        nivelText.textContent = "NIVEL " + nivelActual;
        nivelBox.style.backgroundColor = colores[idx];

        emojis.forEach((e, i) => {
            e.classList.toggle("activo", i === idx);
        });
    }

    slider.addEventListener("input", actualizarUI);
    actualizarUI(); // para el valor inicial

    btnContinuar.addEventListener("click", () => {
        // Guardar el nivel en localStorage
        localStorage.setItem("nivelMalestar", String(nivelActual));
        // Reiniciar índice de ejercicio
        localStorage.setItem("ejercicioActual", "0");

        const urlEjercicio = btnContinuar.dataset.urlEjercicio || "/ejercicio/";
        console.log("Redirigiendo a ejercicio:", urlEjercicio, "con nivel", nivelActual);
        window.location.href = urlEjercicio;
    });
});
