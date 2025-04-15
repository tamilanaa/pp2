import csv
from db import get_connection

def insert_from_console():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO contacts (first_name, last_name, phone_number)
        VALUES (%s, %s, %s)
    """, (first_name, last_name, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added successfully.")

def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 3:
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, phone_number)
                    VALUES (%s, %s, %s)
                """, (row[0], row[1], row[2]))

    conn.commit()
    cur.close()
    conn.close()
    print("Contacts from CSV file have been added.")
