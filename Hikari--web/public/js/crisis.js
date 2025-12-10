const slider = document.getElementById("sliderMalestar");
const nivelText = document.getElementById("nivelText");
const nivelBox = document.getElementById("nivelBox");
const emojiList = document.querySelectorAll("#emojiLine .emoji");
const btnHome = document.getElementById("btnHome");
const btnContinuar = document.getElementById("btnContinuar");
const emojiLine = document.getElementById("emojiLine");
const emojis = document.querySelectorAll(".emoji");

let nivelActual = 1;
/* COLORES DEL NIVEL */
const colores = [
    "#2ecc71", "#55d86c", "#7fe067", "#a8e862", "#d1f05d",
    "#f1c40f", "#e67e22", "#d35400", "#c0392b", "#96281b"
];


slider.addEventListener("input", () => {
    nivelActual = parseInt(slider.value);
    nivelText.textContent = "NIVEL " + nivelActual;
});


/* CASITA → HOME */
btnHome.addEventListener("click", () => {
    window.location.href = "home.html";
});

/* CONTINUAR (futuro flujo DBT) */
btnContinuar.addEventListener("click", () => {
    alert("Aquí va el flujo siguiente según el nivel 🙂");
});

localStorage.setItem("nivelMalestar", nivelActual);
window.location.href = "ejercicio.html";

function corregirThumb() {
    const index = slider.value - 1;

    const emojiWidth = emojis[0].offsetWidth;
    const lineWidth = emojiLine.offsetWidth;

    const espacioEntreEmojis = lineWidth / 9; // 10 emojis → 9 espacios

    const posicionEmoji = index * espacioEntreEmojis + emojiWidth / 2;

    slider.style.setProperty("--thumb-position", posicionEmoji + "px");
}

slider.addEventListener("input", corregirThumb);
window.addEventListener("resize", corregirThumb);

corregirThumb();
