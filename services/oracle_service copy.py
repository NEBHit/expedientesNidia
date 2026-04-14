from config.conexion_oracle import get_oracle_connection

class OracleService:

'''    @staticmethod
    def existe_partida(nro_partida: str) -> bool:
        conn = None
        try:
            print("=====================================================");
            print("Conectandose a Oracle");
            print("=====================================================");

            conn = get_oracle_connection()
            cursor = conn.cursor()

            query = """
                SELECT L.NRO_INMUEBLE,L.PAR_CATASTRAL, L.CIRCUNS, L.SECCION, L.MANZANA_NRO, L.MANZANA_LET, L.PARCELA, L.PARCELA_LET 
                FROM owner_rafam.ING_INMUEBLES L
                WHERE L.NRO_INMUEBLE = :partida
            """

            print("=====================================================");
            print("Por ejecutar sql a Oracle");
            print("PArtida:");
            print(nro_partida);
            print("=====================================================");

            cursor.execute(query, {"partida": nro_partida})
            result = cursor.fetchone()

            print("=====================================================");
            print("Result Oracle");
            print(result);
            print("=====================================================");

            return result is not None

        except Exception as e:
            print("Error consultando Oracle:", e)
            return False

        finally:
            if conn:
                conn.close()


@staticmethod
def obtener_datos_partida(nro_partida: str):
    conn = None
    try:
        conn = get_oracle_connection()
        cursor = conn.cursor()

        query = """
                SELECT L.NRO_INMUEBLE,L.PAR_CATASTRAL, L.CIRCUNS, L.SECCION, L.MANZANA_NRO, L.MANZANA_LET, L.PARCELA, L.PARCELA_LET 
                FROM owner_rafam.ING_INMUEBLES L
                WHERE L.NRO_INMUEBLE = :partida
            """

        cursor.execute(query, {"partida": nro_partida})
        result = cursor.fetchone()

        if not result:
            return None

        # 👇 adaptá estos índices según tu tabla real
        return {
            "partida": result[0],
            "titular": result[1],
            "domicilio": result[2],
            "zona": result[3]
        }

    except Exception as e:
        print("Error obteniendo datos de partida:", e)
        return None

    finally:
        if conn:
            conn.close()             
'''

@staticmethod
def obtener_partida(nro_partida: str):
        conn = None
        try:
            print("===================================")
            print("CONSULTA PARTIDA")
            print("===================================")

            conn = get_oracle_connection()
            cursor = conn.cursor()

            query = """
                SELECT L.NRO_INMUEBLE,L.PAR_CATASTRAL, L.CIRCUNS, L.SECCION, L.MANZANA_NRO, L.MANZANA_LET, L.PARCELA, L.PARCELA_LET 
                FROM owner_rafam.ING_INMUEBLES L
                WHERE L.NRO_INMUEBLE = :partida
            """

            cursor.execute(query, {"partida": nro_partida})
            result = cursor.fetchone()

            # No existe
            if not result:
                return {
                    "existe": False,
                    "datos": None
                }

            # Map dinámico 
            columnas = [col[0].lower() for col in cursor.description]

            data = dict(zip(columnas, result))

            return {
                "existe": True,
                "datos": {
                    "NRO_INMUEBLE": data.get("NRO_INMUEBLE"),
                    "PAR_CATASTRAL": data.get("PAR_CATASTRAL"),
                    "CIRCUNS": data.get("CIRCUNS"),
                    "SECCION": data.get("SECCION"),
                    "MANZANA_NRO": data.get("MANZANA_NRO"),
                    "MANZANA_LET": data.get("MANZANA_LET"),
                    "MANZANA_NRO": data.get("PARCELA"),
                    "MANZANA_NRO": data.get("PARCELA_LET")
                }
            }

        except Exception as e:
            print("Error consultando Oracle:", e)
            return {
                "existe": False,
                "datos": None,
                "error": str(e)
            }

        finally:
            if conn:
                conn.close()