console.log("CONFIGURACION JS CARGADO");

// ====== REFERENCIAS ======
const modalEliminar = document.getElementById("modal-eliminar");
const modalCambiarPass = document.getElementById("modal-cambiar-pass");

const btnEliminar = document.querySelector(".eliminar");           // link "Eliminar cuenta"
const btnCancelarEliminar = document.getElementById("btn-cancelar-eliminar");
const btnCancelarPass = document.getElementById("btn-cancelar-pass");

// ====== ELIMINAR CUENTA ======

// Abrir modal de eliminar cuenta
if (btnEliminar && modalEliminar) {
    btnEliminar.addEventListener("click", function (e) {
        e.preventDefault();
        modalEliminar.style.display = "flex";
    });
}

// Cerrar con botón "Cancelar"
if (btnCancelarEliminar && modalEliminar) {
    btnCancelarEliminar.addEventListener("click", function () {
        modalEliminar.style.display = "none";
    });
}

// Cerrar haciendo clic fuera de la caja blanca
if (modalEliminar) {
    modalEliminar.addEventListener("click", function (e) {
        if (e.target === modalEliminar) {
            modalEliminar.style.display = "none";
        }
    });
}

// ====== CAMBIAR CONTRASEÑA ======

// Estas funciones se usan desde el link del HTML: onclick="abrirCambiarPass()"
window.abrirCambiarPass = function () {
    if (modalCambiarPass) {
        modalCambiarPass.style.display = "flex";
    }
};

window.cerrarCambiarPass = function () {
    if (modalCambiarPass) {
        modalCambiarPass.style.display = "none";
    }
};

// Además, botón "Cancelar" del modal de contraseña
if (btnCancelarPass && modalCambiarPass) {
    btnCancelarPass.addEventListener("click", function () {
        modalCambiarPass.style.display = "none";
    });
}

// Cerrar modal de contraseña clicando fuera
if (modalCambiarPass) {
    modalCambiarPass.addEventListener("click", function (e) {
        if (e.target === modalCambiarPass) {
            modalCambiarPass.style.display = "none";
        }
    });
}
