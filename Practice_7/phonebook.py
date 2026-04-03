import os
import psycopg2
import csv

DEFAULT_ENCODING = "utf-8"
FALLBACK_ENCODING = "cp1251"

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Wr111try#"
    )
    conn.set_client_encoding("UTF8")
    return conn

def ensure_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL UNIQUE
                )
            """)
        conn.commit()

def open_csv_path(path):
    try:
        return open(path, "r", encoding=DEFAULT_ENCODING, errors="strict")
    except UnicodeDecodeError:
        return open(path, "r", encoding=FALLBACK_ENCODING, errors="strict")

def import_from_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "phonebook.csv")
    if not os.path.isfile(csv_path):
        print(f"CSV not found: {csv_path}")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur, open_csv_path(csv_path) as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 2:
                        continue
                    first_name = row[0].strip()
                    phone_number = row[1].strip()
                    if not first_name or not phone_number:
                        continue
                    cur.execute("""
                        INSERT INTO phonebook (first_name, phone_number)
                        VALUES (%s, %s)
                        ON CONFLICT (phone_number) DO NOTHING
                    """, (first_name, phone_number))
            conn.commit()
        print("CSV import successful!")
    except Exception as e:
        print("Error import_from_csv:", e)

def print_rows(rows):
    if not rows:
        print("No results")
        return
    for first_name, phone_number in rows:
        print(f"{first_name} - {phone_number}")

def search():
    print("\nSearch options:")
    print("1. By name contains")
    print("2. By exact phone")
    print("3. By phone prefix")
    print("4. Show all")
    print("0. Back")
    choice = input("Choose: ").strip()
    if choice == "0":
        return

    query = None
    condition = ""
    params = ()
    if choice == "1":
        query = input("Name part: ").strip()
        if not query:
            print("Empty query")
            return
        condition = "WHERE first_name ILIKE %s"
        params = (f"%{query}%",)
    elif choice == "2":
        query = input("Phone exact: ").strip()
        if not query:
            print("Empty query")
            return
        condition = "WHERE phone_number = %s"
        params = (query,)
    elif choice == "3":
        query = input("Phone prefix: ").strip()
        if not query:
            print("Empty query")
            return
        condition = "WHERE phone_number LIKE %s"
        params = (f"{query}%",)
    elif choice == "4":
        condition = ""
        params = ()
    else:
        print("Invalid choice")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                sql = f"""
                    SELECT first_name, phone_number
                    FROM phonebook
                    {condition}
                    ORDER BY first_name, phone_number
                """
                cur.execute(sql, params)
                rows = cur.fetchall()
                print_rows(rows)
    except UnicodeDecodeError as e:
        print("Encoding error in search result:", e)
    except Exception as e:
        print("Error search:", e)

def add_contact():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    if not name or not phone:
        print("Name and phone are required")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO phonebook (first_name, phone_number)
                    VALUES (%s, %s)
                """, (name, phone))
            conn.commit()
        print("Added!")
    except Exception as e:
        print("Error add_contact:", e)

def update():
    print("\nUpdate options:")
    print("1. Find by name")
    print("2. Find by phone")
    print("0. Back")
    mode = input("Choose: ").strip()
    if mode == "0":
        return

    if mode == "1":
        key_name = "first_name"
        key_val = input("Name to update: ").strip()
    elif mode == "2":
        key_name = "phone_number"
        key_val = input("Phone to update: ").strip()
    else:
        print("Invalid choice")
        return

    if not key_val:
        print("Value is required")
        return

    print("\nField to change:")
    print("1. first_name")
    print("2. phone_number")
    field_choice = input("Choose: ").strip()
    if field_choice == "1":
        target_field = "first_name"
    elif field_choice == "2":
        target_field = "phone_number"
    else:
        print("Invalid choice")
        return

    new_value = input(f"New {target_field}: ").strip()
    if not new_value:
        print("New value is required")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE phonebook
                    SET {target_field} = %s
                    WHERE {key_name} = %s
                """, (new_value, key_val))
                updated = cur.rowcount
            conn.commit()
        print(f"Updated {updated} row(s)" if updated else "No matching contact")
    except Exception as e:
        print("Error update:", e)

def delete():
    print("\nDelete options:")
    print("1. By name")
    print("2. By phone")
    print("3. All (confirm)")
    print("0. Back")
    choice = input("Choose: ").strip()
    if choice == "0":
        return

    if choice == "1":
        key_name = "first_name"
        key_val = input("Name to delete: ").strip()
    elif choice == "2":
        key_name = "phone_number"
        key_val = input("Phone to delete: ").strip()
    elif choice == "3":
        ok = input("Drop all rows? Type YES to confirm: ").strip()
        if ok != "YES":
            print("Cancelled")
            return
        key_name = None
        key_val = None
    else:
        print("Invalid choice")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if key_name is None:
                    cur.execute("DELETE FROM phonebook")
                else:
                    cur.execute(f"DELETE FROM phonebook WHERE {key_name} = %s", (key_val,))
                deleted = cur.rowcount
            conn.commit()
        print(f"Deleted {deleted} row(s)" if deleted else "No matching contact")
    except Exception as e:
        print("Error delete:", e)

def main():
    ensure_table()
    try:
        while True:
            print("\n===== PhoneBook =====")
            print("1. Import CSV")
            print("2. Add contact")
            print("3. Update contact")
            print("4. Search contacts")
            print("5. Delete contact")
            print("0. Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                import_from_csv()
            elif choice == "2":
                add_contact()
            elif choice == "3":
                update()
            elif choice == "4":
                search()
            elif choice == "5":
                delete()
            elif choice == "0":
                break
            else:
                print("Invalid choice")
    except KeyboardInterrupt:
        print("\nExit by user")

if __name__ == "__main__":
    main()