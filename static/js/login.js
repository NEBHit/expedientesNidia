document.addEventListener("DOMContentLoaded", function () {
console.log("===============================login.js cargado");
    /* ===============================
       CAPTCHA – recarga sin refresh
       =============================== */
    const btnCaptcha = document.getElementById("btn-refresh-captcha");
    const captchaBox = document.getElementById("captcha-text");

    if (btnCaptcha && captchaBox) {
        btnCaptcha.addEventListener("click", function () {
            fetch("/captcha-refresh")
                .then(response => response.json())
                .then(data => {
                    captchaBox.textContent = data.captcha;

                    // animación suave
                    captchaBox.style.transform = "rotate(0deg)";
                    setTimeout(() => {
                        captchaBox.style.transform = "rotate(-2deg)";
                    }, 150);
                })
                .catch(() => console.error("Error al recargar captcha"));
        });
    }

    /* ===============================
       CONTRASEÑA – mostrar / ocultar
       =============================== */
    const input = document.getElementById("clave");
    const button = document.getElementById("togglePassword");
    const icon = document.getElementById("iconPassword");

    if (input && button && icon) {
        // alternar con click
        button.addEventListener("click", function () {
            if (input.type === "password") {
                mostrar();
            } else {
                ocultar();
            }
        });

        // mostrar mientras se mantiene presionado
        button.addEventListener("mousedown", mostrar);
        button.addEventListener("touchstart", mostrar);

        // ocultar al soltar
        button.addEventListener("mouseup", ocultar);
        button.addEventListener("mouseleave", ocultar);
        button.addEventListener("touchend", ocultar);

        // ocultar al perder foco del input
        input.addEventListener("blur", ocultar);
    }

    function mostrar() {
        input.type = "text";
        icon.classList.remove("bi-eye-fill");
        icon.classList.add("bi-eye-slash-fill");
    }

    function ocultar() {
        input.type = "password";
        icon.classList.remove("bi-eye-slash-fill");
        icon.classList.add("bi-eye-fill");
    }

});

