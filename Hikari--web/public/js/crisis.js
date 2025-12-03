const slider = document.getElementById("sliderMalestar");
const nivelText = document.getElementById("nivelText");
const nivelBox = document.getElementById("nivelBox");
const emojiList = document.querySelectorAll("#emojiLine .emoji");
const btnHome = document.getElementById("btnHome");
const btnContinuar = document.getElementById("btnContinuar");

/* COLORES DEL NIVEL */
const colores = [
    "#2ecc71", "#55d86c", "#7fe067", "#a8e862", "#d1f05d",
    "#f1c40f", "#e67e22", "#d35400", "#c0392b", "#96281b"
];


slider.addEventListener("input", () => {
    const nivel = parseInt(slider.value);

    // Texto
    nivelText.textContent = `NIVEL ${nivel}`;

    // Color de la caja
    nivelBox.style.background = colores[nivel - 1];

    // Emojis
    emojiList.forEach((emoji, index) => {
        emoji.classList.toggle("activo", index + 1 === nivel);
    });
});

/* CASITA → HOME */
btnHome.addEventListener("click", () => {
    window.location.href = "home.html";
});

/* CONTINUAR (futuro flujo DBT) */
btnContinuar.addEventListener("click", () => {
    alert("Aquí va el flujo siguiente según el nivel 🙂");
});
