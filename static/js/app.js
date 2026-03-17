//======================================================================
//Funcion que se usa para realizar la máscara del CUIT/CUIL con formato:
// **-********-*
function handleMask(event, mask) {
    const input = event.target;
    const isDelete =
        event.inputType === "deleteContentBackward" ||
        event.inputType === "deleteContentForward";

    // Valor actual sin separadores
    let digits = input.value.replace(/\D/g, "");

    // Si se ingresó algo que no es número, cancelamos la escritura
    if (!isDelete && !/^\d$/.test(event.data)) {
        input.value = applyMask(digits, mask);
        return;
    }

    if (isDelete) {
        // eliminamos un dígito desde la posición del cursor
        const pos = input.selectionStart;
        const before = input.value.slice(0, pos).replace(/\D/g, "");
        const after  = input.value.slice(pos).replace(/\D/g, "");
        digits = before.slice(0, -1) + after;
    } else {
        digits += event.data; // agregamos el dígito nuevo
    }

    // Limitar a la cantidad de '9'
    const max = (mask.match(/9/g) || []).length;
    digits = digits.slice(0, max);

    // reconstruimos con máscara
    const masked = applyMask(digits, mask);

    // guardamos posición deseada del cursor
    let newPos = calcCursorPos(mask, digits.length);

    input.value = masked;
    input.setSelectionRange(newPos, newPos);
}

function applyMask(digits, mask) {
    let out = "";
    let i = 0;
    for (const m of mask) {
        if (m === "9") out += digits[i++] ?? "";
        else out += digits[i] !== undefined ? m : "";
    }
    return out;
}

// Cursor después del dígito n aplicado a la máscara
function calcCursorPos(mask, nDigits) {
    let count = 0, pos = 0;
    for (let i = 0; i < mask.length; i++) {
        if (mask[i] === "9") {
            count++;
            pos++;
            if (count === nDigits) return pos;
        } else {
            pos++;
        }
    }
    return pos;
}

//Fin máscara
//======================================================================

//======================================================================
//Funcion para cerrar ventanas modales
function cerrarModal(idModal) {
       var modal = document.getElementById(idModal);
       modal.style.display = "none"; //  o modal.classList.remove('show');
       //  Si quieres ocultar el fondo oscuro:
       //  document.querySelector('.modal-overlay').style.display = 'none';
}

//======================================================================
// Función para cerrar el modal al hacer clic fuera de él (opcional)
window.onclick = function(event) {
       var modals = document.getElementsByClassName('modal');
       for (var i = 0; i < modals.length; i++) {
         if (event.target == modals[i]) {
           modals[i].style.display = "none";
         }
       }
}

$(document).ready(function () {
    // MODAL Update INSPECTOR - Muestra los datos del Inspector seleccionado
    $('#update_Inspector').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let apellido = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDINSPECTOREditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#APELLIDOEdit').val(apellido);
    });

    // MODAL ELIMINAR INSPECTOR - Muestra los datos del Inspector seleccionado
    $('#delete_Inspector').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let apellido = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDINSPECTORDelHIDDEN').val(id);

            // Cambiar el título
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Inspector: ' + apellido +  ','  + nombre + ' ?');
            modal.find('#NOMBREDel').val(nombre);
            modal.find('#APELLIDODel').val(apellido);
        
    });


    //======================================================
    //Expedientes
    //======================================================
    $('#add_Expediente').on('shown.bs.modal', function () {
    //carga datos una vez que el modal esta cargado     
        actualizarVisibilidad("");
        actualizarTipoPago("");
    });
    
    $('#update_Expediente').on('shown.bs.modal', function () {
    //carga datos una vez que el modal esta cargado   
        actualizarVisibilidad("Edit");
        actualizarTipoPago("Edit");
    });

    // MODAL Update Expediente
    $('#update_Expediente').on('show.bs.modal', async function (event) {
    //carga datos backend
        let button = $(event.relatedTarget);
        
        let idExpediente = button.data('id');
        let nroLegajo = button.data('nrolegajo');
        let nroExpediente = button.data('nroexpediente');
        let nroPartida = button.data('nropartida');
        let nroExpedienteMesaEntrada = button.data('nroexpedientemesaentr');
        let anioMesaEntrada = button.data('aniomesaentr');
        let sucesion = button.data('sucesion');
        let observaciones = button.data('observaciones');
        let idEstadoExpediente = button.data('idestadoexpediente');

        const tiposObraStr = button.data('tiposobra'); 
        //Limpiar todos los checks de tipo de obras
        document.querySelectorAll('.tipo-obra-check').forEach(chk => {
            chk.checked = false;
        });
        
        let modal = $(this);

        modal.find('#IDEXPEDIENTEEditHIDDEN').val(idExpediente);
        modal.find('#nroLegajoEdit').val(nroLegajo);
        modal.find('#nroExpedienteEdit').val(nroExpediente);
        modal.find('#nroPartidaEdit').val(nroPartida);
        modal.find('#nroExpedienteMesaEntradaEdit').val(nroExpedienteMesaEntrada);
        modal.find('#anioMesaEntradaEdit').val(anioMesaEntrada);
        modal.find('#sucesionEdit').val(sucesion);
        modal.find('#observacionesEdit').val(observaciones);
        modal.find('#idEstadoExpedienteEdit').val(idEstadoExpediente);
        modal.find('#IDESTADOEXPEDIENTEEditHIDDEN').val(idEstadoExpediente);

        //============= Cargar los TIPOS DE OBRAS
        if (tiposObraStr) {
            const tiposArray = tiposObraStr.toString().split(',').map(Number);

            tiposArray.forEach(id => {
                const checkbox = document.getElementById(`tipoObraEdit_${id}`);
                if (checkbox) {
                    checkbox.checked = true;
                }
            });
        }

        //============= Cargar HISTORIAL ESTADOS EXPEDIENTE
        let tabla = document.getElementById("tablaEstadosEdit");
        tabla.innerHTML = `
                <tr>
                    <td colspan="4" class="titulo-tabla"><strong>HISTORIAL DE ESTADOS</strong></td> 
                </tr>
                <tr>          
                    <td class="hr" width="10" align="left"></td>
                    <td class="hr" width="50" align="left"><strong>ESTADO</strong></td>
                    <td class="hr" width="50" align="left"><strong>FECHA CAMBIO</strong></td>
                    <td class="hr" width="50" align="left"><strong>USUARIO</strong></td>
                </tr>
            `;

        //Llamo al backend para traer ESTADOS del EXPEDIENTE
        try {
                const resp = await fetch(`/expediente/${idExpediente}/estados`);
                
                if (!resp.ok) throw new Error("Error al cargar los estados");
                const estados = await resp.json();
                // Renderizo cada estado en la tabla
                estados.forEach((p, idx) => {
                    let style = (idx % 2 === 0) ? "dr" : "sr";
                    
                    let fila = `
                        <td class='${style}' width='10'></td>
                        <td class='${style}' width='50' align='left'>${p.nombre}</td>
                        <td class='${style}' width='50' align='left'>${p.fecha}</td>
                        <td class='${style}' width='50' align='left'>${p.usuario}</td>
                    `;

                    let row = document.createElement("tr");
                    row.id = idx+1;
                    row.innerHTML = fila;
                    tabla.appendChild(row);
            });
            
        } catch (err) {
                console.error("Error cargando estados: ", err);
                alert("No se pudieron cargar los estados");
        }
        
        //============= Cargar PROPIETARIOS
        // Limpio tabla antes de cargar
        tabla = document.getElementById("tablaPropietariosEdit");
        tabla.innerHTML = `
            <tr>          
                <td class="hr" width="10" align="left"></td>
                <td class="hr" width="10" align="left"></td>
                <td class="hr" width="50" align="left"><strong>CUIL/CUIT</strong></td>
                <td class="hr" width="50" align="left"><strong>APELLIDO</strong></td>
                <td class="hr" width="50" align="left"><strong>NOMBRE</strong></td>
                <td class="hr" width="50" align="left"><strong>PPAL.</strong></td>
            </tr>
        `;

        // Llamo al backend para traer propietarios del expediente
        try {
            const respProp = await fetch(`/expediente/${idExpediente}/propietarios`);
            
            if (!respProp.ok) throw new Error("Error al cargar propietarios");
            const propietarios = await respProp.json();

            //alert(JSON.stringify(propietarios));

            // Renderizo cada propietario en la tabla
            propietarios.forEach((p, idx) => {
                let style = (idx % 2 === 0) ? "dr" : "sr";
                let figura = (p.ppal == 1) ? "SI" : "NO";
              
                //alert(JSON.stringify(p));

                let fila = `
                    <td class='${style}' width='2'>
                        <input type='hidden' name='propEdit${idx+1}' id='propEdit${idx+1}' 
                            value='${p.cuil_cuit}/${p.apellido}/${p.nombre}/${p.ppal}/${p.calle}/${p.nroCalle}/${p.piso}/${p.nroDpto}/${p.areaCelular}/${p.nroCelular}/${p.email}'>
                    </td>
                    <td class='${style}' width='10'>
                         <button type='button' class='btn' onclick='deletePropietario("Edit", ${idx+1})' title='Borrar Propietario'>
                                <i class='icon-trash'></i>
                            </button>
                    </td>
                    <td class='${style}' width='50' align='left'>${p.cuil_cuit}</td>
                    <td class='${style}' width='50' align='left'>${p.apellido}</td>
                    <td class='${style}' width='50' align='left'>${p.nombre}</td>
                    <td class='${style}' width='50' align='left'>${figura}</td>
                `;

                let row = document.createElement("tr");
                row.id = "filaPropEdit" + (idx+1);
                row.innerHTML = fila;
                tabla.appendChild(row);

            });

            // Actualizo el contador de filas
            //document.getElementById("idFilaEdit").value = propietarios.length;
        
        } catch (err) {
            console.error("Error cargando propietarios: ", err);
            alert("No se pudieron cargar los propietarios");
        }
       
        //============= Cargar PROPFESIONALES
        // Limpio tabla antes de cargar
        tabla = document.getElementById("tablaProfesionalesEdit");
        tabla.innerHTML = `
            <tr>          
                <td class="hr" width="10" align="left"></td>
                <td class="hr" width="10" align="left"></td>
                <td class="hr" width="50" align="left"><strong>PROFESIONAL</strong></td>
                <td class="hr" width="50" align="left"><strong>PPAL.</strong></td>
            </tr>
        `;

        // Llamo al backend para traer PROFESIONALES del expediente
        try {
            const resp = await fetch(`/expediente/${idExpediente}/profesionales`);
            
            if (!resp.ok) throw new Error("Error al cargar profesionales");
                const profesionales = await resp.json();
                // Renderizo cada profesional en la tabla
                profesionales.forEach((p, idx) => {

                    style = (idx % 2 === 0) ? "dr" : "sr";
                    let ppal = (p.contactoPpal == 1) ? "SI" : "NO";

                    //alert(JSON.stringify(p));

                    fila = `
                        <td class='${style}' width='2'>
                            <input type='hidden' name='profEdit${idx+1}' id='profEdit${idx+1}' 
                                value='${p.idProfesional}/${p.contactoPpal}'>
                        </td>
                        <td class='${style}' width='10'>
                            <button type='button' class='btn'  onclick='deleteProfesional("Edit", ${idx+1})' title='Borrar Profesional'>
                                <i class='icon-trash'></i>
                            </button>
                        </td>
                        <td class='${style}' width='50' align='left'>${p.apellido}, ${p.nombre} /Mat. ${p.matricula}</td>
                        <td class='${style}' width='50' align='left'>${ppal}</td>
                    `;

                    row = document.createElement("tr");
                    row.id = "filaProfEdit" + (idx+1);
                    row.innerHTML = fila;
                    tabla.appendChild(row);
                 });

            // Actualizo el contador de filas
           // document.getElementById("idFilaEdit").value = propietarios.length;
        } catch (err) {
                console.error("Error cargando profesionales: ", err);
                alert("No se pudieron cargar los profesionales");
            }
    });

    

    // MODAL ELIMINAR Expediente - Muestra los datos del Expediente
    $('#delete_Expediente').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nroExpediente = button.data('nroexpediente');
            
            let modal = $(this);
            modal.find('#IDEXPEDIENTEDelHIDDEN').val(id);
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Expediente: ' +  nroExpediente );     
    });

    // MODAL Update EstadoInspeccion - Muestra los datos del Estado de la Inspeccion
    $('#update_EstadoExpediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDESTADOEXPEDIENTEEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR EstadoExpediente - Muestra los datos del Estado del Expediente
    $('#delete_EstadoExpediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDESTADOEXPEDIENTEDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Estado: ' + nombre + ' de los Expediente ?');     
    });

    // MODAL Update EstadoInspeccion - Muestra los datos del Estado de la Inspeccion
    $('#update_EstadoInspeccion').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDESTADOINSPECCIONEditHIDDEN').val(id);
            modal.find('#NOMBREEdit').val(nombre);
            modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR EstadoInspeccion - Muestra los datos del Estado de la Inspeccion
    $('#delete_EstadoInspeccion').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDESTADOINSPECCIONDelHIDDEN').val(id);
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Estado: ' + nombre + ' de las Inspecciones ?');     
    });

    // MODAL Update TipoExpediente - Muestra los datos del Tipo de Expediente
    $('#update_TipoExpediente').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDTIPOEXPEDIENTEEditHIDDEN').val(id);
            modal.find('#NOMBREEdit').val(nombre);
            modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR TipoExpediente - Muestra los datos del Tipo de Expediente
    $('#delete_TipoExpediente').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDTIPOEXPEDIENTEDelHIDDEN').val(id);
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo: ' + nombre + ' de Expediente ?');     
    });
        
    // MODAL Update TipoObra - Muestra los datos del Tipo de Obra
    $('#update_TipoObra').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDTIPOOBRAEditHIDDEN').val(id);
            modal.find('#NOMBREEdit').val(nombre);
            modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR TipoObra - Muestra los datos del Tipo de Obra
    $('#delete_TipoObra').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDTIPOOBRADelHIDDEN').val(id);
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo: ' + nombre + ' de Obra ?');     
    });

    // MODAL Update TipoProfesion - Muestra los datos del Tipo de Profesion
    $('#update_TipoProfesion').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDTIPOPROFESIONEditHIDDEN').val(id);
            modal.find('#NOMBREEdit').val(nombre);
            modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR TipoProfesion - Muestra los datos del Tipo de Profesion
    $('#delete_TipoProfesion').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let descripcion = button.data('descripcion');

            let modal = $(this);
            modal.find('#IDTIPOPROFESIONDelHIDDEN').val(id);
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo de Profesión: ' + nombre + ' ?');     
    });
    
    // MODAL Update Profesional - Muestra los datos del Profesional
    $('#update_Profesional').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let nombre = button.data('nombre');
            let apellido = button.data('apellido');
            let cuil = button.data('cuil');
            let calle = button.data('calle');
            let nrocalle = button.data('nrocalle');
            let piso = button.data('piso');
            let dpto = button.data('dpto');
            let areacel = button.data('areacel');
            let nrocel = button.data('nrocel');
            let idtipoprofesion = button.data('idtipoprof');
            let matricula = button.data('matricula');
            let razonsocial = button.data('razonsocial');
            let mail = button.data('mail');
        
            let modal = $(this);

            modal.find('#IDPROFESIONALEditHIDDEN').val(id);
            modal.find('#apellidoEdit').val(apellido);
            modal.find('#nombreEdit').val(nombre);
            modal.find('#cuil_cuitEdit').val(cuil);
            modal.find('#calleEdit').val(calle);
            modal.find('#nroCalleEdit').val(nrocalle);
            modal.find('#pisoEdit').val(piso);
            modal.find('#dptoEdit').val(dpto);
            modal.find('#areaCelularEdit').val(areacel);
            modal.find('#nroCelularEdit').val(nrocel);
            modal.find('#idTipoProfesionEdit').val(idtipoprofesion);
            //modal.find('.modal-body #IdTipoProfesionEdit').val(idtipoprofesion);

            modal.find('#matriculaEdit').val(matricula);
            modal.find('#razonSocialEdit').val(razonsocial);
            modal.find('#emailEdit').val(mail);

    });

    // MODAL ELIMINAR Profesional - Muestra los datos del Profesional
    $('#delete_Profesional').on('show.bs.modal', function (event) {
            let button = $(event.relatedTarget);
            let id = button.data('id');
            let apellido = button.data('apellido');
            let nombre = button.data('nombre');
            
            let modal = $(this);
            modal.find('#IDPROFESIONALDelHIDDEN').val(id);
            modal.find('.modal-title2').text('¿Estás seguro de eliminar el Profesional: ' + apellido + ', ' + nombre );     
    });
});

