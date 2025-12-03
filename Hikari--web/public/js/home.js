const menuBtn = document.getElementById("menu");
const navbar = document.querySelector(".navbar");
const overlay = document.getElementById("overlay");

menuBtn.addEventListener("change", function() {
    navbar.classList.toggle("active", menuBtn.checked);
    overlay.classList.toggle("active", menuBtn.checked);
    if (menuBtn.checked) {
        navbar.classList.add("active");
    } else {
        navbar.classList.remove("active");
    }
});

document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
        menuBtn.checked = false;
        navbar.classList.remove("active");
    });
});

overlay.addEventListener("click", () => {
    menuBtn.checked = false;
    navbar.classList.remove("active");
    overlay.classList.remove("active");
});

document.querySelectorAll(".navbar a").forEach(item => {
    item.addEventListener("click", () => {
        menuBtn.checked = false;
        navbar.classList.remove("active");
        overlay.classList.remove("active");
    });
});