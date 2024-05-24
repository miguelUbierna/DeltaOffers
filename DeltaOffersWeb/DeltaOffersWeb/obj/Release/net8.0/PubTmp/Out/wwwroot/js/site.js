// Please see documentation at https://learn.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.


function mostrarFormulario() {
    document.getElementById('fondo').style.display = 'block';
    document.getElementById('formulario_flotante').style.display = 'block';

}


function ocultarFormulario() {
    document.getElementById('fondo').style.display = 'none';
    document.getElementById('formulario_flotante').style.display = 'none';
}

var enlaces = document.querySelectorAll('.mostrar_formulario');

enlaces.forEach(function (enlace) {
    enlace.addEventListener("click", function (event) {
        event.preventDefault();

        var ofertaId = enlace.getAttribute('data-oferta-id');
        document.getElementById("ofertaId").value = ofertaId;

        mostrarFormulario();
    });
});


document.getElementById('fondo').addEventListener('click', function () {
    ocultarFormulario();
});

document.getElementById("form").addEventListener("submit", function (event) {
    event.preventDefault();

    var ofertaId = document.getElementById("ofertaId").value;
    var email = document.getElementById("email").value;

    var emailExpReg = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    if (emailExpReg.test(email)) {
        $.ajax({
            type: 'POST',
            url: '/Universidad/SendEmail',
            data: { email: email, ofertaId: ofertaId },
            success: function (response) {
                mostrarAlertaBien();
                document.getElementById('fondo').style.display = 'none';
                document.getElementById('formulario_flotante').style.display = 'none';

            },
            error: function (error) {
                mostrarAlertaMal("Hubo un error al enviar el email.");
            }
        });
    } else {
        mostrarAlertaMal("El correo que has insertado no es válido");
    }
});

function mostrarAlertaMal(mensaje) {
    Swal.fire({
        icon: "error",
        title: mensaje,
        showConfirmButton: false,
        timer: 1500,
        customClass: {
            popup: 'estilo-swal',
        },
    });
}

function mostrarAlertaBien(mensaje) {
    Swal.fire({
        icon: "success",
        title: "El correo se ha enviado correctamente",
        showConfirmButton: false,
        timer: 1500,
        customClass: {
            popup: 'estilo-swal',
        },
    });
}
