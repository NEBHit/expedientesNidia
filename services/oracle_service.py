from config.conexion_oracle import get_oracle_connection

class OracleService:

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
                    SELECT L.NRO_INMUEBLE,L.PAR_CATASTRAL, L.CIRCUNS, L.SECCION, L.MANZANA_NRO, L.MANZANA_LET, L.PARCELA_NRO, L.PARCELA_LET 
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
                    "datos": data
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