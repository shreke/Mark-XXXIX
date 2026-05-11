import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = "postgresql://postgres:RNRFYkfsOrlHExaEErAeHSbZZlakCrVw@monorail.proxy.rlwy.net:48092/railway"

def tms_query(parameters: dict, player=None, speak=None) -> str:
    action = parameters.get("action", "query")
    sql = parameters.get("sql", "")
    params = parameters.get("params", [])

    try:
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        cur = conn.cursor()

        if action == "query":
            cur.execute(sql, params)
            rows = cur.fetchall()
            conn.close()
            if not rows:
                return "No se encontraron resultados."
            return str([dict(r) for r in rows])

        elif action == "write":
            cur.execute(sql, params)
            conn.commit()
            affected = cur.rowcount
            conn.close()
            return f"Operación exitosa. Filas afectadas: {affected}."

        else:
            conn.close()
            return f"Acción desconocida: {action}"

    except Exception as e:
        return f"Error de base de datos: {e}"
