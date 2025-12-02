
const btnEliminar = document.querySelector(".eliminar");
const modal = document.getElementById("modal-eliminar");
const btnCancelarModal = document.querySelector(".btn-cancelar-modal");


btnEliminar.addEventListener("click", function (e) {
    e.preventDefault(); 
    modal.style.display = "flex";  
});


btnCancelarModal.addEventListener("click", function () {
    modal.style.display = "none";  
});

modal.addEventListener("click", function(e){
    if(e.target === modal){
        modal.style.display = "none";
    }
});