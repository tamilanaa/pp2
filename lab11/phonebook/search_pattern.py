import psycopg2
from db import get_connection

def search_by_pattern(pattern):
    try:

        conn = get_connection()
        cur = conn.cursor()

        # shablon i poisk
        query = """
            SELECT * FROM contacts
            WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone_number ILIKE %s;
        """
        like_pattern = f"%{pattern}%"
        cur.execute(query, (like_pattern, like_pattern, like_pattern))
        results = cur.fetchall()

        #vyvod
        for row in results:
            print(row)

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()
