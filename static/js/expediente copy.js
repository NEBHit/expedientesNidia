   
    
  //Estado Expediente
  //Estado de Expediente = "Liquidacion Derecho Construccion Urbanismo"
  ESTADO_LIQ_DER_CONTRUCCION_URB = 11

    function insertarPropietario(){
         idFila=document.getElementById("idFila").value;

         //Leo Datos Personales
         let nombre = document.getElementById("nombre").value;
         let apellido = document.getElementById("apellido").value;
         let cuil_cuit = document.getElementById("cuil_cuit").value;
         let figuraPpal = document.getElementById("figuraPpal").value;
         
         //Leo datos Contacto
         let calle = document.getElementById("calle").value;
         let nroCalle = document.getElementById("nroCalle").value;
         let piso = document.getElementById("piso").value;
         let dpto = document.getElementById("nroDpto").value;
         let areaCelular = document.getElementById("areaCelular").value;
         let nroCelular = document.getElementById("nroCelular").value;
         let email = document.getElementById("email").value;
                  
         if(nombre == ''){alert("El Nombre del Propietario es de ingreso obligatorio."); exit;}
         if(apellido == ''){alert("El Apellido del Propietario es de inghreso obligatorio."); exit;}
         if(cuil_cuit == ''){alert("La CUIL/CUIT del Propietario es de ingreso obligatorio."); exit;}
         if(areaCelular == ''){alert("El Area del Celular es de ingreso obligatorio."); exit;}
         if(nroCelular == ''){alert("El Nro. del Celular es de ingreso obligatorio."); exit;}
         if(email == ''){alert("El Email es de ingreso obligatorio."); exit;}
        
        //De la forma valor= cuil + "/" + apellido + "/" + nombre + "/" + figuraPPal ......;
         valor = cuil_cuit + "/" + apellido + "/" + nombre + "/" + figuraPpal + "/" + calle + "/" + nroCalle + "/" +piso+ "/" +dpto+ "/" +areaCelular+ "/" +nroCelular+ "/" +email;
         
         style = "dr";

         if ((idFila%2) != 0){ style = "sr";}
         if(figuraPpal==0){ ppal= "NO";}else{ ppal= "SI";}
         
         let fila = "<td class='" + style + "' width='2'><input type='hidden' name='prop" + idFila + "' id='prop" + idFila + "' value='" + valor + "'></td><td class='" + style + "'  width='10'><button type='button' class='btn' onClick='deletePropietario(" + idFila + ")' title='Borrar Propietario'><i class='icon-trash'></i></button></td><td class='" + style + "'  width='50' align='left'>" + apellido + "</td><td class='" + style + "'  width='50' align='left'>" + nombre + "</td><td class='" + style + "'  width='50' align='left'>" + cuil_cuit + "</td><td class='" + style + "'  width='50' align='left'>" + ppal + "</td>" ;
                                                
         let btn = document.createElement("TR");
         btn.id=idFila;
         btn.innerHTML=fila;
         document.getElementById("tablaPropietarios").appendChild(btn);

       //  document.getElementById("contFila").value = `${idFila}`; 
         document.getElementById("idFila").value = `${++idFila}`;       
    }

    function deletePropietario(idFila){
        document.getElementById(idFila).remove();
       // document.getElementById("contFila").value = document.getElementById("contFila").value -1;
    }

    function insertarProfesionales(){
        idFila=document.getElementById("idFilaProf").value;

        //Leo Profesional de la forma idprofesiona*Apellido,nombre/ Matticula
        let profesional = document.getElementById("idProfesional").value;
        //Leo ID
        let pos = profesional.indexOf("*");
        let idProfesional = profesional.substr(0, pos);
        profesional = profesional.substr( pos + 1 );

        let contactoPpal = document.getElementById("contactoPpal").value;
                  
        if(profesional == ''){alert("El Profesional es de ingreso obligatorio."); exit;}

        valor= idProfesional + "/" + contactoPpal;
         
        style = "dr";

        if ((idFila%2) != 0){ style = "sr";}
        if(contactoPpal==0){ ppal= "NO";}else{ ppal= "SI";}
        
        let fila = "<td class='" + style + "' width='2'><input type='hidden' name='prof" + idFila + "' id='prof" + idFila + "' value='" + valor + "'></td><td class='" + style + "'  width='10'><button type='button' class='btn' onClick='deleteProfesional(" + idFila + ")' title='Borrar Profesional'><i class='icon-trash'></i></button></td><td class='" + style + "'  width='50' align='left'>" + profesional + "</td><td class='" + style + "'  width='50' align='left'>" + ppal + "</td>" ;
                                                
        let btn = document.createElement("TR");
        btn.id=idFila;
        btn.innerHTML=fila;
        document.getElementById("tablaProfesionales").appendChild(btn);

        //document.getElementById("contFila").value = `${idFila}`; 
        document.getElementById("idFilaProf").value = `${++idFila}`;       
    }

    function deleteProfesional(idFila){
        document.getElementById(idFila).remove();
      // document.getElementById("contFila").value = document.getElementById("contFila").value -1;
    }

   