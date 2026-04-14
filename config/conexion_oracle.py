import oracledb
from dotenv import load_dotenv
import os

oracledb.init_oracle_client(
    lib_dir=r"C:\oracle\oracleinstantclient_21_20"
)

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")

def get_oracle_connection():
    try:
        connection = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASSWORD,
            dsn=ORACLE_DSN
        )
        return connection
    except Exception as e:
        print(f"Error Oracle: {e}")
        return None
    
    
#Servicio de acceso a datos generico      
def query_oracle(sql: str, params: dict = None):
    conn = get_oracle_connection()

    if not conn:
         raise Exception("No se pudo conectar a Oracle")

    cursor = conn.cursor()

    try:
        cursor.execute(sql, params or {})

        columnas = [col[0].lower() for col in cursor.description]

        return [
            dict(zip(columnas, row))
            for row in cursor.fetchall()
        ]

    finally:
        cursor.close()
        conn.close()  