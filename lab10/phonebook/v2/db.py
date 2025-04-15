import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="@GFk%ruw",
        host="localhost",
        port="5432"
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            phone VARCHAR(20)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
