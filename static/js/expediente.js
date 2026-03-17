    //Estado Expediente
    //Estado de Expediente = "DERECHOS DE CONSTRUCCIÓN A PAGAR"
    ESTADO_LIQ_DER_CONTRUCCION_URB = "6"

    function insertarPropietario(sufijo){
        const idFilaInput = document.getElementById("idFila" + sufijo);
        let idFila = Number(idFilaInput.value);

        // Leo Datos Personales
        let nombre = document.getElementById("nombre" + sufijo).value;
        let apellido = document.getElementById("apellido" + sufijo).value;
        let cuil_cuit = document.getElementById("cuil_cuit" + sufijo).value;
        let figuraPpal = document.getElementById("figuraPpal" + sufijo).value;

        // Leo datos Contacto
        let calle = document.getElementById("calle" + sufijo).value;
        let nroCalle = document.getElementById("nroCalle" + sufijo).value;
        let piso = document.getElementById("piso" + sufijo).value;
        let dpto = document.getElementById("nroDpto" + sufijo).value;
        let areaCelular = document.getElementById("areaCelular" + sufijo).value;
        let nroCelular = document.getElementById("nroCelular" + sufijo).value;
        let email = document.getElementById("email" + sufijo).value;

        if(nombre === ''){ alert("El Nombre del Propietario es obligatorio."); return; }
        if(apellido === ''){ alert("El Apellido del Propietario es obligatorio."); return; }
        if(cuil_cuit === ''){ alert("La CUIL/CUIT es obligatoria."); return; }

        let valor = cuil_cuit + "/" + apellido + "/" + nombre + "/" + figuraPpal + "/" +
                    calle + "/" + nroCalle + "/" + piso + "/" + dpto + "/" +
                    areaCelular + "/" + nroCelular + "/" + email;

        let style = (idFila % 2 !== 0) ? "sr" : "dr";
        let ppal = (figuraPpal == 0) ? "NO" : "SI";

        let fila = `
            <td class="${style}" width="2">
                <input type="hidden" name="prop${sufijo}${idFila}" id="prop${sufijo}${idFila}" value="${valor}">
            </td>
            <td class="${style}" width="10">
                <button type="button" class="btn" onclick="deletePropietario('${sufijo}', ${idFila})">
                    <i class="icon-trash"></i>
                </button>
            </td>
            <td class="${style}" width="50">${cuil_cuit}</td>
            <td class="${style}" width="50">${apellido}</td>
            <td class="${style}" width="50">${nombre}</td>
            <td class="${style}" width="50">${ppal}</td>
        `;

        let tr = document.createElement("tr");
        tr.id = "filaProp" + sufijo + idFila;
        tr.innerHTML = fila;

        document.getElementById("tablaPropietarios" + sufijo).appendChild(tr);

        idFilaInput.value = idFila + 1;
    }

    function deletePropietario(sufijo, idFila){
        const fila = document.getElementById("filaProp" + sufijo + idFila);
        if (fila) fila.remove();
    } 

    function insertarProfesionales(sufijo){
        const idFilaInput = document.getElementById("idFilaProf" + sufijo);
        let idFila = Number(idFilaInput.value);

        // Leo Profesional (formato: id*Apellido,Nombre/Matrícula)
        let profesionalFull = document.getElementById("idProfesional" + sufijo).value;

        if(profesionalFull === ''){
            alert("El Profesional es de ingreso obligatorio.");
            return;
        }

        // Extraigo ID
        let pos = profesionalFull.indexOf("*");
        let idProfesional = profesionalFull.substring(0, pos);
        let profesional = profesionalFull.substring(pos + 1);

        let contactoPpal = document.getElementById("contactoPpal" + sufijo).value;

        let valor = idProfesional + "/" + contactoPpal;

        let style = (idFila % 2 !== 0) ? "sr" : "dr";
        let ppal = (contactoPpal == 0) ? "NO" : "SI";

        let fila = `
            <td class="${style}" width="2">
                <input type="hidden" name="prof${sufijo}${idFila}" id="prof${sufijo}${idFila}" value="${valor}">
            </td>
            <td class="${style}" width="10">
                <button type="button" class="btn" onclick="deleteProfesional('${sufijo}', ${idFila})">
                    <i class="icon-trash"></i>
                </button>
            </td>
            <td class="${style}" width="50">${profesional}</td>
            <td class="${style}" width="50">${ppal}</td>
        `;

        let tr = document.createElement("tr");
        tr.id = "filaProf" + sufijo + idFila;
        tr.innerHTML = fila;

        document.getElementById("tablaProfesionales" + sufijo).appendChild(tr);

        idFilaInput.value = idFila + 1;
    }

    function deleteProfesional(sufijo, idFila){
        const fila = document.getElementById("filaProf" + sufijo + idFila);
        if (fila) fila.remove();
    }

    
    //Validaciones
    function validarEstadoExpediente(prefijo = "") {
    //Funcion que valida el ingreso obligatorio de los campos
    //  EstadoExpediente =  Liquidación Derecho Construcción Urbanismo (valor 11)
        const selectEstado = document.getElementById(`idEstadoExpediente${prefijo}`);
        if (!selectEstado) return true;

        // Estado = Liquidación Derecho Construcción Urbanismo
        if (selectEstado.value !== ESTADO_LIQ_DER_CONTRUCCION_URB) return true;

        const selectPago   = document.getElementById(`idTipoPago${prefijo}`);
        const fechaContado = document.getElementById(`fechaPagoContado${prefijo}`);
        const cantCuotas   = document.getElementById(`cantCuotas${prefijo}`);
        const fechaPrimera = document.getElementById(`fechaPagoPrimerCta${prefijo}`);
        const fechaUltima  = document.getElementById(`fechaPagoUltimaCta${prefijo}`);

        if (selectPago.value === "1") {

            if (!fechaContado.value) {
                alert("Debe ingresar la fecha de pago CONTADO.");
                return false;
            }

        } else {

            if (!cantCuotas.value || cantCuotas.value <= 1) {
                alert("La cantidad de cuotas debe ser mayor a 1.");
                return false;
            }

            if (!fechaPrimera.value) {
                alert("Debe ingresar la fecha de la primera cuota.");
                return false;
            }

            if (!fechaUltima.value) {
                alert("Debe ingresar la fecha de la última cuota.");
                return false;
            }
        }

        return true;
    }
   
    function actualizarVisibilidad(prefijo = "") {
        const selectEstado = document.getElementById(`idEstadoExpediente${prefijo}`);
        const rowDerecho = document.getElementById(`rowDerechoConstruccion${prefijo}`);

        if (!selectEstado || !rowDerecho) return;

        const valor = selectEstado.value;

        if (valor === ESTADO_LIQ_DER_CONTRUCCION_URB) {
            rowDerecho.style.display = "block";
        } else {
            rowDerecho.style.display = "none";
        }
    }

    function actualizarTipoPago(prefijo = "") {
        const tipoPago   = document.getElementById(`idTipoPago${prefijo}`);
        const divContado = document.getElementById(`divContado${prefijo}`);
        const divCuotas  = document.getElementById(`divCuotas${prefijo}`);

        const cantCuotas  = document.getElementById(`cantCuotas${prefijo}`);
        const fechaPrimer = document.getElementById(`fechaPagoPrimerCta${prefijo}`);
        const fechaUltima = document.getElementById(`fechaPagoUltimaCta${prefijo}`);

        if (!tipoPago) return;

        if (tipoPago.value == "1") {

            divContado.style.display = "block";
            divCuotas.style.display = "none";

            cantCuotas.disabled = true;
            fechaPrimer.disabled = true;
            fechaUltima.disabled = true;

        } else if (tipoPago.value == "2") {

            divContado.style.display = "none";
            divCuotas.style.display = "flex";

            cantCuotas.disabled = false;
            fechaPrimer.disabled = false;
            fechaUltima.disabled = false;
        }
    }

    document.addEventListener("DOMContentLoaded", function () {

        ["", "Edit"].forEach(prefijo => {

            const estado = document.getElementById(`idEstadoExpediente${prefijo}`);
            const tipoPago = document.getElementById(`idTipoPago${prefijo}`);

            if (!estado && !tipoPago) return;

            estado?.addEventListener("change", () =>
                actualizarVisibilidad(prefijo)
            );

            tipoPago?.addEventListener("change", () =>
                actualizarTipoPago(prefijo)
            );

            // Estado inicial
            actualizarVisibilidad(prefijo);
            actualizarTipoPago(prefijo);
        });

    });