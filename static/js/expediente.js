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
        if(cuil_cuit === ''){ alert("La CUIL/CUIT del Propietario es obligatoria."); return; }
        if((figuraPpal == 1) && ((areaCelular == '')||(nroCelular == ''))){alert("Esta queriendo agregar un Propietario que figura como Contacto Ppal?. Por lo tanto el Télefono de Contacto es de ingreso obligatorio."); return;}
        if(email === ''){ alert("El Email del propietario es obligatoria."); return; }
       
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
        //let profesionalFull = document.getElementById("idProfesional" + sufijo).value;
        let select = document.getElementById("idProfesional" + sufijo);
        let selectedOption = select.options[select.selectedIndex];

        let profesionalFull = selectedOption.value; // esto sigue siendo el string

        if(profesionalFull === ''){
            alert("El Profesional es de ingreso obligatorio.");
            return;
        }


        // Extraigo ID
        let pos = profesionalFull.indexOf("*");
        let idProfesional = profesionalFull.substring(0, pos);
        let profesional = profesionalFull.substring(pos + 1);

        let email = selectedOption.dataset.email;

        let contactoPpal = document.getElementById("contactoPpal" + sufijo).value;

        let valor = idProfesional + "/" + contactoPpal + "/" + email;

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

   //=======================================================================
   // Manejo de relacion entre tipos de expediente y tipos de obras
   //======================================================================= 
   const restriccionesPorTipoExp = {
        1: {
            prohibidas: [9],
            incompatibilidades: {
                2: [7],
                4: [7],
                6: [7]
            }
        },
        2: {
            soloPermitidas: [9]
        }
    };

    function actualizarRestricciones(sufijo) {
        const tipoExp = document.getElementById(`idTipoExpediente${sufijo}`).value;
        const reglas = restriccionesPorTipoExp[tipoExp];

        const checks = document.querySelectorAll(`#tiposObrasContainer${sufijo} .tipo-obra-check`);

        // resetear
        checks.forEach(chk => {
            chk.disabled = false;
            chk.parentElement.style.opacity = "1";
        });

        if (!reglas) return;

        // PROHIBIDAS (ej: obra 9 en tipo 1)
        if (reglas.prohibidas) {
            reglas.prohibidas.forEach(id => {
                const chk = document.getElementById(`tipoObra${sufijo}_${id}`);
                if (chk) {
                    chk.checked = false;
                    chk.disabled = true;
                    chk.parentElement.style.opacity = "0.5";
                }
            });
        }

        // SOLO PERMITIDAS (tipo 2)
        if (reglas.soloPermitidas) {
            checks.forEach(chk => {
                const id = parseInt(chk.value);
                if (!reglas.soloPermitidas.includes(id)) {
                    chk.checked = false;
                    chk.disabled = true;
                    chk.parentElement.style.opacity = "0.5";
                }
            });
        }

        // INCOMPATIBILIDADES (tipo 1)
        const seleccionados = Array.from(checks)
            .filter(chk => chk.checked)
            .map(chk => parseInt(chk.value));

        if (reglas.incompatibilidades) {
            seleccionados.forEach(sel => {

                // directas
                if (reglas.incompatibilidades[sel]) {
                    reglas.incompatibilidades[sel].forEach(prohibido => {
                        const chk = document.getElementById(`tipoObra${sufijo}_${prohibido}`);
                        if (chk && !chk.checked) {
                            chk.disabled = true;
                            chk.parentElement.style.opacity = "0.5";
                        }
                    });
                }

                // inversas
                for (const [key, values] of Object.entries(reglas.incompatibilidades)) {
                    if (values.includes(sel)) {
                        const chk = document.getElementById(`tipoObra${sufijo}_${key}`);
                        if (chk && !chk.checked) {
                            chk.disabled = true;
                            chk.parentElement.style.opacity = "0.5";
                        }
                    }
                }
            });
        }
    }

    document.querySelectorAll('.tipo-obra-check').forEach(chk => {
    chk.addEventListener('change', function() {
            const sufijo = this.id.includes("Edit") ? "Edit" : "";
            actualizarRestricciones(sufijo);
        });
    });

    document.querySelectorAll('[id^="idTipoExpediente"]').forEach(select => {
        select.addEventListener('change', function() {
            const sufijo = this.id.includes("Edit") ? "Edit" : "";
            actualizarRestricciones(sufijo);
        });
    });

   
    //Validar TipoEzxpediente/TipoObra antes de enviar el submit
    function validarCombinacionesTipoExpTipoObraAntesDeEnviar(sufijo) {
        const tipoExp = document.getElementById(`idTipoExpediente${sufijo}`).value;
        const reglas = restriccionesPorTipoExp[tipoExp];

        const checks = document.querySelectorAll(`#tiposObrasContainer${sufijo} .tipo-obra-check`);

        const seleccionados = Array.from(checks)
            .filter(chk => chk.checked)
            .map(chk => parseInt(chk.value));

        if (!reglas) return true;

        // PROHIBIDAS (ej: obra 9)
        if (reglas.prohibidas) {
            const conflicto = seleccionados.find(o => reglas.prohibidas.includes(o));
            if (conflicto) {
                alert(`No se puede seleccionar la obra ${conflicto} para este tipo de expediente`);
                return false;
            }
        }

        // SOLO PERMITIDAS (tipo 2)
        if (reglas.soloPermitidas) {
            const conflicto = seleccionados.find(o => !reglas.soloPermitidas.includes(o));
            if (conflicto) {
                alert(`Solo se permite seleccionar la obra ${reglas.soloPermitidas.join(", ")}`);
                return false;
            }
        }

        // INCOMPATIBILIDADES (ej: 2 y 7)
        if (reglas.incompatibilidades) {
            for (let i = 0; i < seleccionados.length; i++) {
                for (let j = i + 1; j < seleccionados.length; j++) {

                    const a = seleccionados[i];
                    const b = seleccionados[j];

                    if (reglas.incompatibilidades[a]?.includes(b)) {
                        alert(`No se puede combinar ${a} con ${b}`);
                        return false;
                    }

                    if (reglas.incompatibilidades[b]?.includes(a)) {
                        alert(`No se puede combinar ${b} con ${a}`);
                        return false;
                    }
                }
            }
        }

        return true;
    }


    function leerTiposSeleccionados(sufijo) {
        const seleccionados = [];

        document.querySelectorAll(`#tiposObrasContainer${sufijo} .tipo-obra-check:checked`)
            .forEach(cb => {
                seleccionados.push(cb.value);
            });

        if (seleccionados.length === 0) {
            alert("Debe seleccionar al menos un Tipo de Obra");
            return false;
        }

        document.getElementById(`idTipoObra${sufijo}`).value = JSON.stringify(seleccionados);

        return true;
    }
    //=========================================================================
    // FIN
    //=========================================================================
   

    //=========================================================================
    // VALIDAR PARTIDA CONTRA RAFAM AL INTANTE DEL TIPEADO
    //=========================================================================
    async function ejecutarValidacionRAFAM(sufijo) {

        const input = document.getElementById(`nroPartida${sufijo}`);
        const partida = input.value.trim();
        if (!partida) return;

        const alerta = document.getElementById(`alertaPartida${sufijo}`);
        const datosDiv = document.getElementById(`datosCatastrales${sufijo}`);
        const hidden = document.getElementById(`catastroRafamHidden${sufijo}`);

        try {
            const response = await fetch(`/validar_partida?nroPartida=${partida}`);
            const data = await response.json();

            if (!data.existe) {
                alerta.style.display = "block";
                alerta.innerText = data.mensaje;

                datosDiv.innerHTML = "";
                if (hidden) hidden.value = "";
            } else {
                alerta.style.display = "none";

                const d = data.datos;

                const circ = d.circuns ?? "";
                const sec = d.seccion ?? "";
                const mz = d.manzana_nro ?? "";
                const mzlet = d.manzana_let ?? "";
                const par = d.parcela_nro ?? "";
                const parlet = d.parcela_let ?? "";

                const catastro = `${circ}-${sec}-MZ ${mz}${mzlet}-${par}${parlet}`;

                datosDiv.innerHTML = `
                    <div class="form-group col-md-6 mb-2">
                        <label><strong>CATASTRO RAFAM</strong></label>
                        <input type="text" class="form-control" value="${catastro}" disabled />
                    </div>
                `;

                if (hidden) hidden.value = catastro;
            }

        } catch (error) {
            console.error("Error validando partida", error);
        }
    }
    //=========================================================================
    // FIN
    //=========================================================================