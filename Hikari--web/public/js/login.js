const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const errorMsg = document.getElementById("error-pass");
const btnLogin = document.getElementById("btn-login");

btnLogin.addEventListener("click", function (e) {
    e.preventDefault();

    if (emailInput.value.trim() === "" || passwordInput.value.trim() === "") {
        errorMsg.textContent = "Por favor completa todos los campos.";
        return;
    }

    if (emailInput.value === "test@gmail.com" && passwordInput.value === "12345") {
        errorMsg.textContent = "";
        window.location.href = "../paginas/home.html";
    } else {
        errorMsg.textContent = "Correo o contraseña incorrecta.";
    }
});


