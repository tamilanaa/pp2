from db import get_connection

def paginate_query(table_name, limit, offset):
    try:

        connection = get_connection()
        con = connection.cursor()

        query = f"SELECT * FROM {table_name} LIMIT %s OFFSET %s;"
        con.execute(query, (limit, offset))
        
        rows = con.fetchall()

        for row in rows:
            print(row)

    except Exception as e:
        print("Error:", e)
    finally:
        if connection:
            con.close()
            connection.close()
