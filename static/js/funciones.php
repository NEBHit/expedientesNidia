<?php
// Funciones
function buscar($word)
        {
            // Abrimos el archivo para leerlo ....
            $abierto =fopen("texto.txt","r");   
            
            // Inicializamos la variable $i y la flag $encontrado ....
            $i = 0;
            $encontrado = 0;
            
            // Mientras no sea FIN DE ARCHIVO ...                                                                                         
            while (!feof ($abierto))
                {
                        // Guardo una linea completa en la variable $linea ....
                        $linea = fgets ($abierto);
                        // Copio la linea al array
                        $array[$i] = $linea;
                        // Si encuentro la palabra dentro de esa linea ....
                        if (eregi($word, $array[$i]))
                            {
                                // Enciendo la flag ... sino sigue apagada ...
                                $encontrado = 1;
                            }
                        // Incremento el contador del indice
                        $i++;
                }      
            
            // Cierro el archivo ...       
            fclose ($abierto);   
            
            // Pongo en 0 $i (por las dudas)
            $i = 0;
            
            print ("<img src='inc/search.jpg'>");
            // Si la flag esta ON significa que encontramos al menos una repeticion de la palabra buscada ...
            if ($encontrado == 1)
                {
                    // Cabeceras
                    print ("<center><h3>Resultado de la Busqueda</h3></center>");
                    print ("<center><h4>Palabra buscada: </h4><h2>$word</h2></center>");
                    // Recien aca empiezo a imprimir el contenido del archivo ...
                    for ($i=0; $i <=count($array); $i++)
                        {
                            // Reemplazo la palabra original por la misma palabra + el tag HTML
                            $reemplazo = "<font size = 5><strong>".$word."</strong></font>";
                            $nuevacadena = str_replace ($word, $reemplazo, $array[$i]);
                            // Mostramos la nueva cadena ...
                            print ($nuevacadena);     
                        }                  
                }
            // Si la flag esta OFF significa que no hay ni una repeticion de la palabra buscada ...
            else
                {
                    print ("<center><h3>No se han encontrado resultados</h3></center>");
                }                             
        }      
		
function cadena($palabra)
	{
	// Inicializamos la variable $i, $cad y la flag $b ....
	//  $b=0;
	// $cad="";
	// $i=0;
	//  $longitud=0;
	   // Tomo la longitud de la Cadena ....
	  // $longitud=strlen($palabra)-1;
	   // Truncamos la cadena a 100 caracteres ....
	   // if($longitud > 100)
	      //{$longitud = 100; }
		  
	       //for($i=0; $i<=$longitud; $i++)
		   //{  
			  //$l=substr($palabra,$i,1);
			  		       // obtengo un caracter de la cadena en la posicion $i .... 	
             // if ((ord($l) >= 65) and (ord($l) <= 90)) 
			  //	 {$cad = $cad.$l;
			   //  }
			  // else {
				 //   if ((ord($l) >= 97) and (ord($l) <= 122))
					//   {$cad = $cad.$l;
		              // }
						 // Comparamos el caracter obtenido con los valores comprendidos en la estructura de control if ..... 
					//else { 
						//  if ((ord($l) >= 48) and (ord($l) <= 57))
						  //   {$cad = $cad.$l;
		        		//	  }
						 // else {
							//    if ((ord($l) == 32) or (ord($l) == 34) or (ord($l) == 95))
							  //     { $cad = $cad.$l;
							//	   }
								  // Si el caracter no coincide con los valores propuestos seteo el flag en 1, para forzar la salida del while......
									
							//	}
						//	}	
				//	 }
					
//			 }
            $cad=$palabra; 
		    return $cad;
			 // Retorna el valor de la cadena
	}	

function numero($numero)
	{
	// Inicializamos la variable $i, $cad y la flag $b ....
	  $b=0;
	  $cad="";
	  $i=0;
	  $longitud=0;
	   // Tomo la longitud de la Cadena ....
	   $longitud=strlen($numero)-1;
	   // Truncamos la cadena a 100 caracteres ....
	    if($longitud > 100)
	      {$longitud = 100; }
		  
	       for($i=0; $i<=$longitud; $i++)
		   {  
			  $num=substr($numero,$i,1);
			  		       // obtengo un caracter de la cadena en la posicion $i .... 	
            
						 // Comparamos el caracter obtenido con los valores comprendidos en la estructura de control if ..... 
					if ((ord($num) >= 48) and (ord($num) <= 57))
						     {$cad = $cad.$num;
		        			  }
						
		  }
		  if ($cad == "")
		      {$cad = 0;}
            
		    return $cad;
			 // Retorna el valor de la cadena
	}
	
function toHtml($entra){
$traduce=array('�' => '&Aacute;', '�' => '&Eacute;', '�' => '&Iacute;', '�' => '&Oacute;', '�' => '&Uacute;', '�' => '&Ntilde;', '�' => '&aacute;' , '�' => '&eacute;' , '�' => '&iacute;' , '�' => '&oacute;' , '�' => '&uacute;' , '�' => '&ntilde;', '�' => '&deg;', '-' => '&ndash;','�' => '&quot;','�' => '&quot;', '�' => '&ndash;', '�' => '&uuml;', '�' => '&ndash;');
$sale=strtr( $entra , $traduce );
return $sale;
}

//------------------------------------------------------------------------------------------------------------------------------------------------
//Funciones genericas agregadas por Nidia
//------------------------------------------------------------------------------------------------------------------------------------------------

function validarRequerido($valor){
	//Funcion que valida si un campo requerido en el formulario es ingresado o no. 
	//Retorna verdadero si $valor no es una cadena vacia y falso en cc.
	
   if(trim($valor) == ''){ //trim elimina los espacios vacios en una cadena de caracteres
      return false;
   }else{
      return true;
   }
}

function validarNumero($valor){
	//Funcion que valida si el parametro $valor es un numero. 
	//Retorna verdadero si es entero y falso en cc.
	
	//filter_var(): funcion para validar. Recibe tres par�metros:
	// 1 - el primero es el valor a validar o filtrar ( parametro $valor)
	// 2 - el segundo el tipo de validaci�n, (FILTER_VALIDATE_INT, funcion para validar los n�meros enteros)
	// 3 - el tercero es un array con reglas opcionales, (parametro $opciones=null)
	//Aclaracion tercer parametro:
	//si deseo limitar los valores a ingresar, debo especificarlo en esta variable que es un array, indicando:
	//el m�nimo y m�ximo de rango, por ejemplo si es una edad puedo indicar entre que rango de edades estoy validando (edad entre 3 y 100 a�os)
	
	//elimino caracteres de espacio en el parametro de ingreso.
   $valor = trim($valor);
   
   if(filter_var($valor, FILTER_VALIDATE_INT, $opciones=null) === FALSE){
      return false;
   }else{
      return true;
   }
}

function validarEntero($valor, $opciones=null){
	//Funcion que valida si el parametro $valor es un entero. 
	//Retorna verdadero si es entero y falso en cc.
	
	//filter_var(): funcion para validar. Recibe tres par�metros:
	// 1 - el primero es el valor a validar o filtrar ( parametro $valor)
	// 2 - el segundo el tipo de validaci�n, (FILTER_VALIDATE_INT, funcion para validar los n�meros enteros)
	// 3 - el tercero es un array con reglas opcionales, (parametro $opciones=null)
	//Aclaracion tercer parametro:
	//si deseo limitar los valores a ingresar, debo especificarlo en esta variable que es un array, indicando:
	//el m�nimo y m�ximo de rango, por ejemplo si es una edad puedo indicar entre que rango de edades estoy validando (edad entre 3 y 100 a�os)
	
	//elimino caracteres de espacio en el parametro de ingreso.
	$valor = ltrim($valor);
	
   
  //  mensajeAlerta("El CUIT medio 1 " . filter_var($valor, FILTER_VALIDATE_INT, $opciones));
   

   if(filter_var($valor, FILTER_VALIDATE_INT, $opciones) === FALSE){
//	mensajeAlerta("El CUIT medio " . $valor);
      return false;
   }else{
//	mensajeAlerta("BIEN!! " );
      return true;
   }
   
}

function validarFloat($valor, $opciones=null){
	//Funcion que valida si el paramtro $valor es un float. 
	//Retorna verdadero si es un float y falso en cc.
	
	//filter_var(): funcion para validar. Recibe tres par�metros:
	// 1 - el primero es el valor a validar o filtrar ( parametro $valor)
	// 2 - el segundo el tipo de validaci�n, (FILTER_VALIDATE_FLOAT, funcion para validar los n�meros flotantes)
	// 3 - el tercero es un array con reglas opcionales, (parametro $opciones=null)
	
	//Aclaracion tercer parametro:
	//si deseo limitar los valores a ingresar, debo especificarlo en esta variable que es un array, indicando:
	
	
	//elimino caracteres de espacio en el parametro de ingreso.
   $valor = trim($valor);
   
   if(filter_var($valor, FILTER_VALIDATE_FLOAT, $opciones) === FALSE){
      return false;
   }else{
      return true;
   }
}

function validarEmail($valor){
	//Funcion que valida si $valor es una direccion de mail correctamente formada.
	//Se valildan direcciones de correo electr�nico con la sintaxis de RFC 822
	//Retorna verdadero si esta correctamente formado y falso en cc.
	
    if(filter_var($valor, FILTER_VALIDATE_EMAIL) === FALSE){
       return false;
    }else{
       return true;
    }
 }

function validarEmailHotmail($valor){
	//Funcion que valida si el parametro $valor es una direccion de mail correspondiente a HOTMAIL. $valor debe ser una direccion de mail correctamente formada por lo tanto 
	//antes de llamar a esta funcion se deberia validar por fuera que $valor es una direccion de mail correctamente formada. Para esto usar la funcion validarEmail
	//Retorna verdadero si esta correctamente formado y falso en cc.

/*echo "posicion: ";
echo strpos($valor, "@");
echo "==";
echo "subcadena: ";*/

	//me quedo con el proveedor de la direccion de mail
	$subCadenaHotmail=substr($valor, (strpos($valor, "@") + 1),7);

//echo $subCadenaHotmail;

	//convierto la subcadena a mayuscualas
	$subCadenaHotmail= convertirStrMayusculas($subCadenaHotmail);

/*echo "Mayusculas: ";
echo $subCadenaHotmail;*/

	if(( $subCadenaHotmail != "") && ($subCadenaHotmail == "HOTMAIL")){
       return true;
    }else{
       return false;
    }
 }
 
function validarCaracterEspecial($valor){
	//Funcion que valida si el parametro $valor es una cadena de caracteres corespondiente a solo letras. 
	//Retorna verdadero si esta correctamente formado y falso en cc.
	
	
	//eliminamos los espacios en blanco y transformamos a mayusculas
	$valor = strtoupper(trim($valor));
	
	$pos1 = strpos($valor, ";");
	$pos2 = strpos($valor, "'");
	$pos3 = strpos($valor, "/");
	$pos4 = strpos($valor, "|");
	$pos5 = strpos($valor, "*");
		
	
	if(($pos1 === false) && ($pos2 === false) && ($pos3 === false) && ($pos4 === false) && ($pos5 === false)) {
				return true;
    }else{
       			return false;
    }
 }
 
function validarSinSQL($valor){
	//Funcion que valida si el parametro $valor no contiene ninguna palabra clave de SQL. 
	//Retorna verdadero si esta correctamente formado y falso en cc.
	
	
	//eliminamos los espacios en blanco y transformamos a mayusculas
	$valor = strtoupper(trim($valor));
	
	$pos1 =  strpos($valor,"SELECT");
	$pos2 =  strpos($valor,"INSERT");
	$pos3 =  strpos($valor,"DROP");
	$pos4 =  strpos($valor,"UPDATE");
	$pos5 =  strpos($valor,"FROM");
		
	if(($pos1 === false) && ($pos2 === false) && ($pos3 === false) && ($pos4 === false) && ($pos5 === false)) {
				return true;
    }else{
       			return false;
    }
	
 }
 
function validarCadenaCaracteres($valor){
	 //Funcion que retorna verdadero si la cadena de caracteres ingresado no contiene caracteres que pueden da�ar la DB
	 //Retorna verdadero si esta bien formada y false en caso contrario.
	 
	//Validar requerido
	if (!validarRequerido($valor)){
			return false;
	}elseif (!validarCaracterEspecial($valor)){
		//validar solo letras
			return false;
	}elseif (!validarSinSQL($valor)){
		//validar sentencia SQL
			return false;
	}else{
			return true;		
	}
	
}


 function validarFormatoCUIL($valor){
	//Funcion que valida si el parametro $valor corresponde al formato de CUIT/CUIL xx-xxxxxxxx-x, donde x sean numeros solo numeros
	//Retorna verdadero si esta correctamente formado y falso en cc
	
   $valor = trim($valor);
   $subCadena = '';
   
   //validamos si la longitud de la cadena es de 13 caracteres
   if (strlen($valor) != 13){
	   return false;
   }else{
	   //validar si los dos primeros caracteres son numeros
	   $subCadena=substr($valor, 0, 2);

	   if (!validarEntero($subCadena, null)){
		   return false;
	   }else{
			   //validar primer guion
			   $subCadena=substr($valor, 2, 1);
			   if ( $subCadena != "-"){
				   	return false;
			   }else{
				   //validar numero del medio. 8 caracteres.
				   $subCadena=substr($valor, 3, 8);
				   $primernro=substr($subCadena, 0, 1);
				   if($primernro == 0){
					$subCadena=substr($subCadena, 1,8);
			   }	
				   
			   if (!validarEntero($subCadena,null)) {
					   return false;
			   }else{
					   //validar segundo guion
					   $subCadena=substr($valor,11,1);
					   if ($subCadena != "-") {
						   return false;
					   }else{
						   //validamos el ultimo caracter si es numero
						   $subCadena=substr($valor,12,1);
						   if (!validarEntero($subCadena,null)){
							   return false;
						   }else{
							   return true;	
						   }
					   }
				   }
			   }
		   } 
   }
}
  
 
function validarTelefono ($valor){
 //Funcion que valida el formato de telefono: area-numero
 //en el caso de ser un celular el formato es:
 //			area-15numero
 //Mascara: xxxx-15xxxxxx o xxxx-xxxxxx (13 caracteres como m�ximo)
 
 
/*echo $valor;
echo "==";
echo strlen($valor);
echo "==";
*/ 
 //validar si la cantidad de caracteres se corrsponde con la mascara
 if(strlen($valor) > 13){ //no respecta el m�ximo de caracteres permitidos. No valido por menor porque puede ser un telefono particular  o celular y tampoco se el formato del area
	 return false;
 }else{
	 //validar si existe el - separando area de telefono
	$pos =  strpos($valor,"-");
	if ($pos == false){
//echo "no se encontro el - de separacion de area";	
		return false;
	}else{	
 		$subCadena=substr($valor,0,$pos); //me quedo con el �rea telef�nica

/*echo "pos";
echo strpos($valor,"-");
echo "area";
echo $subCadena;
echo "==";
echo "area";
echo "==";
echo strlen($subCadena);
echo "==";
*/
		if ((strlen($subCadena) > 4) || (strlen($subCadena) < 2) ||(!validarEntero($subCadena, null))){
/*echo "longitud de  area incorrecta";
echo "==";*/
				return false;
		}else{
				//validar el nro. de t�lefono. 
				$subCadena=substr($valor,$pos + 1, strlen($valor));
/*echo "Nro telefono";
echo $subCadena;
echo "==";	
echo strlen($subCadena);
echo "==";
*/				
				//valido que los caracteres ingresados para el telefono, corespondan a un numero y que la longitud 
				//corresponda a un telefono particular o celular.
				//if((strlen($subCadena) != 6) && (strlen($subCadena) != 8)){
/*echo "longitud de  nro telefonico incorrecta";
echo "==";*/					
				if(strlen($subCadena) < 6){
					return false;
				}elseif(strlen($subCadena) > 8 ){	
					return false;
				}elseif(!validarEntero($subCadena, null)){
/*echo " nro telefonico no es un nro.";
echo "==";*/						
					return false;
				} elseif ((strlen($subCadena) == 8) && (substr($subCadena,0,2) != "15")){
/*echo " es un nro celular, pero no antepone el 15. Invalido";
echo substr($subCadena,0,1);
echo "==";*/					
					return false;
				}else{
					return true;	
				}
		}
	}
 }	
 }
 
function convertirStrMayusculas($valor){
	 //Funcion que transforma una cadena de caracteres en mayuscula y elimina los espacios en blanco
	 //retorna la cadena recibida en Mayuscuala y sin espacios en blanco
	 
	 $valor = trim($valor);
	 if ($valor != ""){
		 $valor = strtoupper($valor);
	 }
 }
 
function convertirStrMinusculas($valor){
	 //Funcion que transforma una cadena de caracteres en minuscula y elimina los espacios en blanco
	 //retorna la cadena recibida en Minuscula y sin espacios en blanco
	 
	 $valor = trim($valor);
	 if ($valor != ""){
		 $valor = strtolower($valor);
	 }
 }

  
function mensajeAlerta($message){
	 echo '<script>
	 		alert ("' . $message . '");
			window.history.back();
			</script>';
	 exit;
 }
 
function getFechaActual(){
//Funcion que lee la fecha actual del sistema y retorna en el formato mySQL 

	$fechaActual=date("Y-m-d H:i:s");

	return $fechaActual;
}

function getSoloFechaActual(){
//Funcion que lee la fecha actual del sistema y retorna en el formato mySQL 

	$fechaActual=date("d-m-Y");

	return $fechaActual;
}


function anioActual(){
//Funcion que lee la fecha actual del sistema y retorna el a�o 
	$fechaActual=getSoloFechaActual();
	$anio=date("Y", strtotime($fechaActual));

	return $anio;
}

function getEstado($estado){

	if(($estado=="T")|| ($estado=="")) {
			return "EN TRAMITE";
	}elseif(($estado=="S")|| ($estado=="s")){
			return "APROBADO";
	}else{
			return "NO APROBADO";
	}
}

function getEnvioIngresosPublicos($recibo){
	if($recibo=="S"){
			return "SI";
	}else{
			return "NO";
	}
}

function validarEdicion($estado){
//Funcion que valida si es posible editar una solicitud.
//Una solicitud es editable si esta en Estado S (APROBADA) o T(TRAMITE)
//Retorna verdadero si es p�sible editar la solicitu y false en cc.

	if (($estado == "S") || ($estado == "T")){
		return true;	
	}else{
		return false;	
	}
}

//=====================================================================================================
//Funciones especificas del m�dulo conexiones
//Nidia
//=====================================================================================================
 
function validarRequeridoSolicitante($nom, $ape, $razonsoc){
	//Funcion que valida que el usuario cargue Nombre y Apellido o Razon Social.
	//Posibles casos de carga:
	//	Nombre 		Apellido	s	Razon Social
	//	SI			SI				SI
	//	SI			SI				NO
	//	NO			NO				SI
	
	if((trim($nom) == "")&&(trim($ape) != "")){
		mensajeAlerta("Ingrese el Nombre del solicitante.");
	}elseif((trim($nom)!="") && (trim($ape) == "")){
		mensajeAlerta("Ingrese el Apellido del solicitante.");
	}elseif((trim($razonsoc)=="") && (trim($nom)=="") and (trim($ape)=="")){
		mensajeAlerta("Ingrese Nombre y Apellido y/o Raz�n Social del solicitante.");	
	}elseif ((trim($nom) != "") && (!validarCadenaCaracteres($nom))){
		mensajeAlerta("Ingrese un Nombre del solicitante v�lido.");		
	}elseif((trim($ape)!="")&&(!validarCadenaCaracteres($ape))){
		mensajeAlerta("Ingrese un Apellido del solicitante v�lido.");
	}elseif((trim($razonsoc) != "") && ((!validarCaracterEspecial($razonsoc)) || (!validarSinSQL($razonsoc))) ){
		mensajeAlerta("Ingrese la Raz�n Social del solicitante correctamente. ");	
	}elseif((trim($ape) != "") && (trim($nom) == trim($ape))){
		mensajeAlerta("El Nombre y el Apellido del solicitante no pueden ser iguales.");	
	}
 }
 
 //==================================================================================================================
 //Mandar mails del modulo Panel . Oficina Catastro
 //==================================================================================================================
function enviarMailCatastro($nombre, $dni,$domiReal, $domiConec, $telefono, $mail, $observaciones,$aprobado){

		//Armando encabezado mail
	    $dest =  $mail;
	  	$subject="Pedido de Conexion de Luz Domiciliaria";
	   	$from_email = "pedidoconexion@9dejulio.gov.ar";
	   
	   //Encabezados
		$headers = "MIME-Version: 1.0\r\n"; 
		//ruta del mensaje desde origen a destino 
		$headers .= "Return-path:" .$from_email."\r\n"; 
		$headers .= "From: " . $from_email . "\n";
		//$headers .= "BCC: jorge@9deJulio.gov.ar, j_secreto@hotmail.com"."\r\n"; 
		$headers .= "Content-Type: text/plain". "\r\n"; 


	   //Cuerpo del mensaje
	 	$msg = "MUNICIPALIDAD DE 9 DE JULIO - OFICINA DE CATASTRO. \n";
		$msg.= "SOLICITUD DE CONEXION DE LUZ DOMICILIARIA \n";
		$msg.= "--------------------------------------------------------------------------------- \n";
		
		if ($aprobado == "S"){ //Permitir mandar el mail si el ESTADO es S 			
			$msg.= "SUS DATOS FUERON VERIFICADOS CORRECTAMENTE. \n";
			$msg.= "\n";
			$msg.= "EN LOS PROXIMOS DIAS RECIBIRA UN E-MAIL CON EL PERMISO DE CONEXION Y LA BOLETA DE PAGO \n";
			$msg.= "DESDE LA OFICINA DE INGRESOS PUBLICOS, PARA FINALIZAR EL TRAMITE. \n";
			$msg.= "\n";
		}elseif ($aprobado == "N"){
			//Cuerpo del mensaje
			$msg.= "SUS DATOS FUERON VERIFICADOS. \n";
			$msg.= "\n";
			$msg.= "SU TRAMITE HA SIDO DESAPROBADO. \n";
			$msg.= "\n";
		}

		$msg.= "MUCHAS GRACIAS. \n";
		$msg .= "\n";
		
		$msg.= "---------------------------------------------------------------------------------- \n";

		//Completo el cuerpo del mensaje
		$msg .= "Datos Solicitante: " . "\n";
		$msg .= "---------------------------------------------------------------------------------- \n";
		$msg.= "NOMBRE:   ". $nombre."\n";
		$msg.= "CUIT/CUIL:  ". $dni ."\n";
		$msg.= "TELEFONO: ". $telefono. "\n";
		$msg.= "E-MAIL:    ". $mail ."\n";
		$msg.= "DOMICILIO REAL:    ". $domiReal ."\n";
		$msg.= "DOMICILIO CONEXION:  ". $domiConec ."\n";
		
		if (trim($observaciones) != ""){
				$msg.= "OBSERVACIONES:  ".$_POST['OBSERVACIONES']."\n";   
		}
		
		$msg.= "                                              \n";
		$msg.= "L�neas Rotativas: 2317-610000 \n";  
		$msg.= "Municipalidad de 9 de Julio \n";
		$msg.= "DIRECCION DE SISTEMAS DE INFORMACION \n\n";
	
		//Texto plano
		/*$body = "--$boundary\r\n";
		$body .= "Content-Type: text/plain; charset=ISO-8859-1\r\n";
		$body .= "Content-Transfer-Encoding: base64\r\n\r\n"; 
		$body .= chunk_split(base64_encode($msg)); 
		*/
		$body .= $msg;
		
		
		//Enviamos el mensaje
	 	if (mail($dest, $subject, $body, $headers)){
			echo '<script language="javascript">
				alert("Se ha enviado correctamente el E-MAIL al Contribuyente.");
				if (window.history.replaceState) { // verificamos disponibilidad
 				   window.history.replaceState(null, null, window.location.href);
				}
				</script>';
		}else{
			echo '<script language="javascript">
				alert("Los datos fueron enviados correctamente, pero no hemos podido enviarle el E-MAIL de confirmaci�n. Por favor comuniquese con el municipio .... Gracias !");
				if (window.history.replaceState) { // verificamos disponibilidad
 				   window.history.replaceState(null, null, window.location.href);
				}
			</script>';
		}

}

/*function enviarMailIngresoPublicos($pdf, $boleta, $nombre, $dni, $mail){
//Funcion que envia un mail al Contribuyente para notificar que su tramite termino y que tiene disponible el comprobante de permiso de conexion y la boleta de pago
//$pdf = comprobante de permiso de conexion
//$boleta = boleta de pago
 global $_POST;
 
		//Armando encabezado mail
	    $dest =  $mail;
	  	$subject="Pedido de Conexion de Luz Domiciliaria";
	   	$from_email = "ingresos@9dejulio.gov.ar";		
	   
	   		
	   //Cuerpo del mensaje
	 	$msg = "MUNICIPALIDAD DE 9 DE JULIO - OFICINA DE CATASTRO. \n";
		$msg.= "SOLICITUD DE CONEXION DE LUZ DOMICILIARIA \n";
		$msg.= "--------------------------------------------------------------------------------- \n";
		$msg.= "\n";
		$msg.= "SUS DATOS FUERON VERIFICADOS CORRECTAMENTE. \n";
		$msg.= "\n";
		$msg.= "SE ADJUNTA COMPROBANTE DE PERMISO DE CONEXION AUTORIZADO PARA PRESENTAR DONDE CORRESPONDA Y BOLETA PARA EL PAGO. \n";
		$msg.= "CUALQUIER INQUIETUD ACERCARSE AL MUNICIPIO A LA OFICINA DE CATASTRO O LLAMAR TELEFONICAMENTE. \n";
		$msg.= "\n";
		$msg.= "MUCHAS GRACIAS. \n";
		$msg .= "\n";
		$msg.= "---------------------------------------------------------------------------------- \n";
		//Completo el cuerpo del mensaje
		$msg .= "Datos Solicitante: " . "\n";
		$msg .= "---------------------------------------------------------------------------------- \n";
		$msg.= "NOMBRE:   ". $nombre."\n";
		$msg.= "CUIT/CUIL:  ". $dni ."\n";
		$msg.= "                                              \n";
		$msg.= "L�neas Rotativas: 2317-610000 \n";  
		$msg.= "Municipalidad de 9 de Julio \n";
		$msg.= "DIRECCION DE SISTEMAS DE INFORMACION \n\n";
	
		
 		$boundary = md5("pera");
	   
	   //Encabezados
		$headers = "MIME-Version: 1.0\r\n"; 
		$headers .= "Return-path:" .$from_email."\r\n"; 
		$headers .= "From:".$from_email."\r\n"; 
		///$headers .= "Reply-To: ".$reply_to_email."" . "\r\n";
		$headers .= "BCC: jorge@9deJulio.gov.ar, nidia@9deJulio.gov.ar, j_secreto@hotmail.com"."\r\n"; 
		$headers .= "Content-Type: multipart/mixed; boundary = $boundary\r\n\r\n"; 
		//ruta del mensaje desde origen a destino 
			
				   
		//Texto plano
		$body = "--$boundary\r\n";
		$body .= "Content-Type: text/plain; charset=ISO-8859-1\r\n";
		$body .= "Content-Transfer-Encoding: 8bit\r\n\r\n"; 
		//$body .= chunk_split(base64_encode($msg)); 
		$body .= $msg;

		//===========Archivo Permiso de conexion============
		//adjunto pdf
		$attachment = chunk_split(base64_encode($pdf));
		
		$body .= "--$boundary\r\n";
		$body .="Content-Type: application/pdf; name=". "permisoConexion.pdf"."\r\n";
		$body .="Content-Disposition: attachment; filename="."permisoConexion.pdf"."\r\n";
		$body .="Content-Transfer-Encoding: base64\r\n";
		$body .="X-Attachment-Id: ".rand(1000,99999)."\r\n\r\n"; 
		$body .= $attachment;

		//===============Archivo adjunto BOLETA========================= 
		move_uploaded_file($_FILES['FILEBOLETA']['tmp_name'], "./".$boleta); //sube el archivo al servidor
		$file_size        = $_FILES['FILEBOLETA']['size'];
		$file_type        = $_FILES['FILEBOLETA']['type'];
		$file_error       = $_FILES['FILEBOLETA']['error'];
		
		//Leer el archivo y codificar el contenido para armar el cuerpo del email
		$handle = fopen($boleta, "r");
		$content = fread($handle, $file_size);
		fclose($handle);
		$attachmentBoleta = chunk_split(base64_encode($content));
		unlink($boleta);
		

		$body .= "--$boundary\r\n";
		$body .="Content-Type: application/pdf; name=".$boleta."\r\n";
		$body .="Content-Disposition: attachment; filename=".$boleta."\r\n";
		$body .="Content-Transfer-Encoding: base64\r\n";
		$body .="X-Attachment-Id: ".rand(1000,99999)."\r\n\r\n"; 
		$body .= $attachmentBoleta; 
		
						
		//Enviamos el mensaje
		if (mail($dest, $subject, $body, $headers)){
			echo '<script language="javascript">
				alert("Se ha enviado correctamente el E-MAIL al Contribuyente.");
				if (window.history.replaceState) { // verificamos disponibilidad
 				   window.history.replaceState(null, null, window.location.href);
				}
				</script>';
		}else{
			echo '<script language="javascript">
				alert("No hemos podido enviar el E-MAIL al Contribuyente.");
				if (window.history.replaceState) { // verificamos disponibilidad
 				   window.history.replaceState(null, null, window.location.href);
				}
			</script>';
		}
}*/

function enviarMailIngresoPublicos($pdf, $boleta, $nombre, $dni, $mail,$path, $nameBoleta, $namePermiso){
//Funcion que envia un mail al Contribuyente para notificar que su tramite termino y que tiene disponible el comprobante de permiso de conexion y la boleta de pago
//$pdf = comprobante de permiso de conexion
//$boleta = boleta de pago
 global $_POST;

		//Armando encabezado mail
	    $dest =  $mail;
	  	$subject="Pedido de Conexion de Luz Domiciliaria";
	   	$from_email = "ingresos@9dejulio.gov.ar";		
	   		
	   //Cuerpo del mensaje
	   $msg ="<html>
				<head>
				<title>Comprobantes</title>
				</head>
				<body>
				<br>";
	 	$msg.= "<p>MUNICIPALIDAD DE 9 DE JULIO - OFICINA DE INGRESOS PUBLICOS. </p>";
		$msg.= "<p>SOLICITUD DE CONEXION DE LUZ DOMICILIARIA </p>";
		$msg.= "---------------------------------------------------------------------------------------------------------------------------------------- ";
		$msg.= "<p>SUS DATOS FUERON VERIFICADOS CORRECTAMENTE. </p>";
		$msg .= "<BR>";
		
		$msg .= "<p>DATOS SOLICITANTE: " . "</p>";
		$msg.= "<p>NOMBRE:   ". $nombre."</p>";
		$msg.= "<p>CUIT/CUIL:  ". $dni ."</p>";
		$msg .= "<BR>";
		
		$msg.= "<p>PARA DESCARGAR EL PERMISO DE CONEXION DE LUZ DOMICILIARIA INGRESAR <a href='https://apps.9dejulio.gov.ar/conexiones/" . $path . $namePermiso . "'> aqu�</a></p>";
		$msg.= "<p>PARA DESCARGAR LA BOLETA DE PAGO INGRESAR <a href='https://apps.9dejulio.gov.ar/conexiones/" . $path . $boleta . "'> aqu�</a></p>";
		$msg .= "<BR>";
		$msg.= "<p>CUALQUIER INQUIETUD ACERCARSE AL MUNICIPIO A LA OFICINA DE CATASTRO O LLAMAR TELEFONICAMENTE. </p>";
		$msg.= "<br>";
		$msg.= "<p>MUCHAS GRACIAS. </p>";
		
	
		//$msg.= "<p>En caso de no poder descargar el permiso de conexion ingresar<a href='https://apps.9dejulio.gov.ar/conexiones/pruebaOld/" . $path . $namePermiso . "'> aqu�</a></p>";
//		$msg.= "<p>En caso de no poder descargar la boleta de pago ingresar<a href='https://apps.9dejulio.gov.ar/conexiones/pruebaOld/" . $path . $boleta . "'> aqu�</a></p>";
		
		$msg.= "<br>";
	    $msg.= "<p>L�neas Rotativas: 2317-610000 </p>";  
		$msg.= "<p>Municipalidad de 9 de Julio </p>";
		$msg.= "<p>DIRECCION DE SISTEMAS DE INFORMACION </p><br>";
		
		$msg.= "</body>
				</html>";
		
/*		$link = '
			<html>
			<head>
			<title>Comprobantes</title>
			</head>
			<body>
			<br>
			<p>En caso de no poder descargar el permiso de conexion ingresar<a href="https://apps.9dejulio.gov.ar/conexiones/pruebaOld/' . $path . $namePermiso . '"> aqu�</a></p>
			<p>En caso de no poder descargar la boleta de pago ingresar<a href="https://apps.9dejulio.gov.ar/conexiones/pruebaOld/' . $path . $boleta . '"> aqu�</a>
			</p>
			</body>
			</html>';
*/			
 		$boundary = md5("pera");
	   
	   //Encabezados
		$headers = "MIME-Version: 1.0\r\n"; 
		$headers .= "Return-path:" .$from_email."\r\n"; 
		$headers .= "From:".$from_email."\r\n"; 
		///$headers .= "Reply-To: ".$reply_to_email."" . "\r\n";
//		$headers .= "BCC: jorge@9deJulio.gov.ar, jorgesecreto@gmail.com, j_secreto@hotmail.com"."\r\n"; 
//		$headers .= "Content-Type: multipart/mixed; boundary =  $boundary\r\n\r\n";
		$headers .= "Content-Type: text/html; boundary =  $boundary\r\n\r\n";

		//ruta del mensaje desde origen a destino 
				   
		//Texto plano
//		$body = "--$boundary\r\n";
//		$body .= "Content-Type: text/html; charset=ISO-8859-1\r\n";
		//$body .= "Content-Transfer-Encoding: 8bit\r\n\r\n"; 
		//$body .= chunk_split(base64_encode($msg)); 
		$body .= $msg;
		

		//===========Archivo Permiso de conexion============
		//adjunto pdf
/*		$attachment = chunk_split(base64_encode($pdf));
		
		$body .= "--$boundary\r\n";
		//$body .="Content-Type: application/pdf; name=". "permisoConexion.pdf"."\r\n";
		$body .="Content-Type: application/pdf; name=". $namePermiso ."\r\n";
		//$body .="Content-Disposition: attachment; filename="."permisoPdf.pdf"."\r\n";
		$body .="Content-Disposition: attachment; filename=". $namePermiso ."\r\n";
		$body .="Content-Transfer-Encoding: base64\r\n";
		$body .="X-Attachment-Id: ".rand(1000,99999)."\r\n\r\n"; 
		$body .= $attachment;

		//===============Archivo adjunto BOLETA========================= 
		//move_uploaded_file($_FILES['FILEBOLETA']['tmp_name'], "./".$boleta); //sube el archivo al servidor
		$file_size        = $_FILES['FILEBOLETA']['size'];
		$file_type        = $_FILES['FILEBOLETA']['type'];
		$file_error       = $_FILES['FILEBOLETA']['error'];
		
		//Leer el archivo y codificar el contenido para armar el cuerpo del email
		$handle = fopen($path.$nameBoleta, "r");
		$content = fread($handle, $file_size);
		fclose($handle);
		$attachmentBoleta = chunk_split(base64_encode($content));
		unlink($boleta);

		$body .= "--$boundary\r\n";
		$body .="Content-Type: application/pdf; name=".$boleta."\r\n";
		$body .="Content-Disposition: attachment; filename=".$boleta."\r\n";
		$body .="Content-Transfer-Encoding: base64\r\n";
		$body .="X-Attachment-Id: ".rand(1000,99999)."\r\n\r\n"; 
		$body .= $attachmentBoleta; 
		
		//agrego link
		$body .= "--$boundary\r\n";
		$body .= "Content-Type: text/html; charset=ISO-8859-1\r\n";
		//$body .= "Content-Transfer-Encoding: 8bit\r\n\r\n"; 
		$body .= $link;
			
*/		
		//Enviamos el mensaje
		if (mail($dest, $subject, $body, $headers)){
			echo '<script language="javascript">
				alert("Se ha enviado correctamente el E-MAIL al Contribuyente.");
				if (window.history.replaceState) { // verificamos disponibilidad
 				   window.history.replaceState(null, null, window.location.href);
				}
				</script>';
		}else{
			echo '<script language="javascript">
				alert("No hemos podido enviar el E-MAIL al Contribuyente.");
				if (window.history.replaceState) { // verificamos disponibilidad
 				   window.history.replaceState(null, null, window.location.href);
				}
			</script>';
		}
}


function getEstadoAbreviado($estado){
//Funcion que retorna el caracter correspondiente a la cadena de caracteres recibida como parametro	

	switch ($estado) {
		case "APROBADO":
		  $estado="S";
		  break;
		case "NO APROBADO":
		  $estado="N";	
		  break;
		case "EN TRAMITE":
		  $estado="T";	
		  break; 
	 }
	 return $estado;
}

//==================================================================================================================
//Mandar mails del modulo Panel . OficinaIngresos Publicos
//==================================================================================================================
function enviarMailIPublico($nombre, $dni,$domiReal, $domiConeC, $telefono, $mail, $pdfgenerado){
//Esta funcion por el momento no esta en uso

		//Armando encabezado mail
	    $dest =  $mail;
		$subject="Pedido de Conexion de Luz Domiciliaria";
	   	$from_email = "pedidoconexion@9dejulio.gov.ar";
	   
	   //Encabezados
		$headers = "MIME-Version: 1.0\r\n"; 
		//ruta del mensaje desde origen a destino 
		$headers .= "Return-path:" .$from_email."\r\n"; 
		$headers .= "From: " . $from_email . "\n";
//		$headers .= "BCC: jorge@9deJulio.gov.ar, nidia@9deJulio.gov.ar, j_secreto@hotmail.com"."\r\n"; 
		$headers .= "Content-Type: multipart/mixed; boundary = $boundary\r\n\r\n"; 



	   //Cuerpo del mensaje
	 	$msg = "MUNICIPALIDAD DE 9 DE JULIO - OFICINA DE INGRESOS PUBLICOS. \n";
		$msg.= "SOLICITUD DE CONEXION DE LUZ DOMICILIARIA \n";
		$msg.= "--------------------------------------------------------------------------------- \n";
		
		$msg.= "SUS TRAMITE HA FINALIZADO. \n";
		$msg.= "\n";
		$msg.= "ENVIAMOS PDF Y BOLETA PARA PODER ABONAR EL IMPORTE DE CONEXION. \n";
		$msg.= "POR CUALQUIER INQUIETUD DIRIJASE A LA OFICINA DE INGRESOS PUBLICOS DEL MUNICIPIO. \n";
		$msg.= "\n";
		
		$msg.= "MUCHAS GRACIAS. \n";
		$msg .= "\n";
		
		$msg.= "---------------------------------------------------------------------------------- \n";

		//Completo el cuerpo del mensaje
		$msg .= "Datos Solicitante: " . "\n";
		$msg .= "---------------------------------------------------------------------------------- \n";
		$msg.= "NOMBRE:   ". $nombre."\n";
		$msg.= "CUIT/CUIL:  ". $dni ."\n";
		$msg.= "TELEFONO: ". $telefono. "\n";
		$msg.= "E-MAIL:    ". $mail ."\n";
		$msg.= "DOMICILIO REAL:    ". $domiReal ."\n";
		$msg.= "DOMICILIO CONEXION:  ". $domiConec ."\n";
		
		$msg.= "                                              \n";
		  
		$msg.= "Municipalidad de 9 de Julio \n";
		$msg.= "DIRECCION DE SISTEMAS DE INFORMACION \n\n";
	
			
		$filename = "autorizacion.pdf";
		$pdfdoc = $pdfgenerado->Output('', 'S');
		$attachment = chunk_split(base64_encode($pdfdoc),76,"\n");
		
		//Texto plano
		$body = "--$boundary\r\n";
		$body .= "Content-Type: text/plain; charset=ISO-8859-1\r\n";
		$body .= "Content-Transfer-Encoding: base64\r\n\r\n"; 
		//$body .= chunk_split(base64_encode($messageTexto));
		$body .= chunk_split($msg,76,"\n");

		//Adjunto
		$body .= "--$boundary\r\n";
		$body .="Content-Type: $file_type; name=".$filename."\r\n";
		$body .="Content-Disposition: attachment; filename=".$filename."\r\n";
		$body .="Content-Transfer-Encoding: base64\r\n";
		$body .="X-Attachment-Id: ".rand(1000,99999)."\r\n\r\n"; 
		$body .= $attachment . "\r\n"; 
		
		//Enviamos el mensaje
	 	if (mail($dest, $subject, $body, $headers)){
			echo '<script language="javascript">
				alert("Los datos fueron enviados Correctamente.");
				window.history.go(-2); 
				</script>';
		}

}

?>