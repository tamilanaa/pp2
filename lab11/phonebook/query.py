from db import get_connection

def query_contacts():
    print("Query contacts by:")
    print("1. First name")
    print("2. Last name")
    print("3. All contacts")

    option = input("Choose an option (1-3): ")

    conn = get_connection()
    cur = conn.cursor()

    if option == "1":
        name = input("Enter first name: ")
        cur.execute("SELECT * FROM contacts WHERE first_name = %s", (name,))
    elif option == "2":
        name = input("Enter last name: ")
        cur.execute("SELECT * FROM contacts WHERE last_name = %s", (name,))
    else:
        cur.execute("SELECT * FROM contacts")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()
