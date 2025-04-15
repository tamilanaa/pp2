import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="postgres",         
        user="postgres",        
        password="@GFk%ruw",
        host="localhost",
        port="5432"
    )

# tables
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            current_level INTEGER DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            username TEXT REFERENCES users(username),
            score INTEGER,
            level INTEGER,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# user or create new 
def get_or_create_user():
    username = input("enter your namee: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT current_level FROM users WHERE username = %s", (username,))
    result = cur.fetchone()

    if result:
        level = result[0]
        print(f"welcome, {username}! your current level is: {level}")
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s)", (username,))
        conn.commit()
        level = 0
        print(f"new user is created: {username}")

    cur.close()
    conn.close()
    return username, level

#score and level
def save_game(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_score (username, score, level) VALUES (%s, %s, %s)
    """, (username, score, level))
    cur.execute("""
        UPDATE users SET current_level = %s WHERE username = %s
    """, (level, username))
    conn.commit()
    cur.close()
    conn.close()
    print("saved)")
