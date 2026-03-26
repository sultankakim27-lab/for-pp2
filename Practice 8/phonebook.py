from connect import get_connection

def main():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Upsert (добавить или обновить)
    cur.execute("CALL upsert_contact(%s, %s, %s)",
                ('Ali', 'Khan', '87771234567'))

    # 2. Поиск
    cur.execute("SELECT * FROM search_contacts(%s)", ('Ali',))
    print("Search result:")
    for row in cur.fetchall():
        print(row)

    # 3. Пагинация
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (5, 0))
    print("\nPaginated:")
    for row in cur.fetchall():
        print(row)

    # 4. Bulk insert
    cur.execute("""
        CALL bulk_insert_contacts(%s, %s, %s)
    """, (
        ['John', 'Jane'],
        ['Doe', 'Smith'],
        ['87770000000', 'invalid']
    ))

    # 5. Delete
    cur.execute("CALL delete_contact(%s, %s, %s)",
                ('John', 'Doe', None))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()