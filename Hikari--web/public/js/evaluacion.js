let nivel = parseInt(localStorage.getItem("nivelMalestar"));
let ejercicioActual = parseInt(localStorage.getItem("ejercicioActual"));


document.getElementById("btnMejor").addEventListener("click", () => {

    
    if (nivel >= 8) {
        nivel = 5; 
        localStorage.setItem("nivelMalestar", nivel);
        localStorage.setItem("ejercicioActual", 0);
    }

    window.location.href = "ejercicio.html";
});


document.getElementById("btnSiguientePaso").addEventListener("click", () => {

    
    if (nivel >= 8) {
        ejercicioActual++;
        localStorage.setItem("ejercicioActual", ejercicioActual);
    }

    window.location.href = "ejercicio.html";
});
