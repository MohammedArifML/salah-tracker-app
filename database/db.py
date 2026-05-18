import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# -----------------------------------
# Create Tables
# -----------------------------------

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    # Prayers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prayers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            prayer_date TEXT,
            fajr INTEGER,
            zuhr INTEGER,
            asr INTEGER,
            maghrib INTEGER,
            isha INTEGER
        )
    """)

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    conn.commit()
    conn.close()

# -----------------------------------
# Seed Default Users
# -----------------------------------

def seed_users():

    conn = get_connection()

    cursor = conn.cursor()

    default_users = [

        ("admin", "admin123", "admin"),

        ("arif", "123", "user"),

        ("maryam", "123", "user"),

        ("zeenat", "123", "user"),

        ("aisha", "123", "user")

    ]

    for user in default_users:

        try:

            cursor.execute("""
                INSERT INTO users (
                    username,
                    password,
                    role
                )
                VALUES (?, ?, ?)
            """, user)

        except:
            pass

    conn.commit()

    conn.close()

# -----------------------------------
# Add User
# -----------------------------------

def add_user(user_name):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (user_name)
            VALUES (?)
        """, (user_name,))

        conn.commit()

    except:
        pass

    conn.close()


# -----------------------------------
# Get Usernames
# -----------------------------------

def get_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT username
        FROM users
        ORDER BY username
    """)

    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]


# -----------------------------------
# Authenticate User
# -----------------------------------

def authenticate_user(
    username,
    password
):
    username = username.lower()
    
    conn = get_connection()

    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT
            username,
            role
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user

# -----------------------------------
# Get Existing Record
# -----------------------------------

def get_prayer_record(user_name, prayer_date):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM prayers
        WHERE user_name = ?
        AND prayer_date = ?
    """, (user_name, prayer_date))

    row = cursor.fetchone()

    conn.close()

    return row


# -----------------------------------
# Insert Prayer
# -----------------------------------

def insert_prayer(
    user_name,
    prayer_date,
    fajr,
    zuhr,
    asr,
    maghrib,
    isha
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prayers (
            user_name,
            prayer_date,
            fajr,
            zuhr,
            asr,
            maghrib,
            isha
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        prayer_date,
        fajr,
        zuhr,
        asr,
        maghrib,
        isha
    ))

    conn.commit()
    conn.close()


# -----------------------------------
# Update Prayer
# -----------------------------------

def update_prayer(
    user_name,
    prayer_date,
    fajr,
    zuhr,
    asr,
    maghrib,
    isha
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE prayers
        SET
            fajr = ?,
            zuhr = ?,
            asr = ?,
            maghrib = ?,
            isha = ?
        WHERE user_name = ?
        AND prayer_date = ?
    """, (
        fajr,
        zuhr,
        asr,
        maghrib,
        isha,
        user_name,
        prayer_date
    ))

    conn.commit()
    conn.close()


# -----------------------------------
# User History
# -----------------------------------

def get_user_history(user_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            prayer_date,
            fajr,
            zuhr,
            asr,
            maghrib,
            isha
        FROM prayers
        WHERE user_name = ?
        ORDER BY prayer_date DESC
        LIMIT 7
    """, (user_name,))

    rows = cursor.fetchall()

    conn.close()

    return rows

# -----------------------------------
# Get All Records for User
# -----------------------------------

def get_all_user_records(user_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            prayer_date,
            fajr,
            zuhr,
            asr,
            maghrib,
            isha
        FROM prayers
        WHERE user_name = ?
        ORDER BY prayer_date
    """, (user_name,))

    rows = cursor.fetchall()

    conn.close()

    return rows

# -----------------------------------
# Daily Completion Totals
# -----------------------------------

def get_daily_completion_data(user_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            prayer_date,
            (
                fajr +
                zuhr +
                asr +
                maghrib +
                isha
            ) as total_completed
        FROM prayers
        WHERE user_name = ?
        ORDER BY prayer_date
    """, (user_name,))

    rows = cursor.fetchall()

    conn.close()

    return rows

# -----------------------------------
# Get User Role
# -----------------------------------

def get_user_role(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT role
        FROM users
        WHERE username = ?
    """, (username,))

    role = cursor.fetchone()

    conn.close()

    if role:
        return role[0]

    return None