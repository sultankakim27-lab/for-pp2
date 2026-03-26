# 📘 Practice 8 — PostgreSQL Functions & Stored Procedures (PhoneBook)

## 📌 Overview

This project extends the PhoneBook application by moving core logic into the PostgreSQL database using **functions** and **stored procedures**.

The goal is to practice:

* PL/pgSQL programming
* Functions and procedures
* Input validation
* Pagination
* Working with PostgreSQL from Python (`psycopg2`)

---

## 🧩 Features Implemented

### ✅ 1. Pattern Search Function

Search contacts by name, surname, or phone number.

```sql
SELECT * FROM search_contacts('Ali');
```

---

### ✅ 2. Upsert Procedure

Insert a new contact or update an existing one.

```sql
CALL upsert_contact('Ali', 'Khan', '87771234567');
```

---

### ✅ 3. Bulk Insert with Validation

Insert multiple contacts using arrays with phone validation.

* Uses loop (`FOR`)
* Validates phone using regex
* Skips invalid entries

```sql
CALL bulk_insert_contacts(
    ARRAY['John', 'Jane'],
    ARRAY['Doe', 'Smith'],
    ARRAY['87770000000', 'invalid']
);
```

---

### ✅ 4. Pagination Function

Retrieve contacts using LIMIT and OFFSET.

```sql
SELECT * FROM get_contacts_paginated(5, 0);
```

---

### ✅ 5. Delete Procedure

Delete contact by name/surname or phone.

```sql
CALL delete_contact('Ali', 'Khan', NULL);
CALL delete_contact(NULL, NULL, '87771234567');
```

---

## 📂 Project Structure

```
Practice8/
├── phonebook.py        # Main Python script
├── functions.sql       # PostgreSQL functions
├── procedures.sql      # PostgreSQL procedures
├── config.py           # Database configuration
├── connect.py          # Database connection
└── README.md           # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Create Table

```sql
CREATE TABLE contacts (
    name VARCHAR,
    surname VARCHAR,
    phone VARCHAR
);
```

---

### 2. Run SQL Scripts

Execute in PostgreSQL:

* `functions.sql`
* `procedures.sql`

---

### 3. Configure Database

Edit `config.py`:

```python
DB_NAME = "phonebook"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

---

### 4. Run Python Script

```bash
python phonebook.py
```

---

## 🛠 Technologies Used

* PostgreSQL
* PL/pgSQL
* Python
* psycopg2

---

## ⚠️ Notes

* Use `SELECT` to call functions
* Use `CALL` to execute procedures
* Phone validation uses regex: `^[0-9]{10,15}$`
* Procedures handle insert/update/delete logic

---

## 🚀 GitHub

To push the project:

```bash
git add .
git commit -m "Add Practice8 - PhoneBook with functions and stored procedures"
git push origin main
```

---

## ✅ Status

✔ All required tasks completed:

* Pattern search function
* Upsert procedure
* Bulk insert with validation
* Pagination function
* Delete procedure

---

## 📚 Resources

* PostgreSQL Documentation: https://www.postgresql.org/docs/
* psycopg2 Documentation: https://www.psycopg.org/docs/
* PL/pgSQL Tutorial: https://neon.com/postgresql/postgresql-plpgsql
