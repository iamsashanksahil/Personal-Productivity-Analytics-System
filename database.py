import mysql.connector
from tkinter import messagebox

# ==============================
# DATABASE CONFIGURATION
# ==============================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",      # Enter your MySQL password
    "port": 3306
}

DATABASE_NAME = "productivity_db"


# ==============================
# CREATE DATABASE
# ==============================

def create_database():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"
        )

        connection.commit()

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        messagebox.showerror(
            "Database Error",
            f"Unable to create database.\n\n{err}"
        )


# ==============================
# DATABASE CONNECTION
# ==============================

def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DATABASE_NAME,
        port=DB_CONFIG["port"]
    )


# ==============================
# CREATE TABLES
# ==============================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- Tasks ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(

        task_id INT AUTO_INCREMENT PRIMARY KEY,

        task_name VARCHAR(200) NOT NULL,

        category VARCHAR(50),

        priority ENUM(
            'High',
            'Medium',
            'Low'
        ),

        status ENUM(
            'Pending',
            'Completed'
        ) DEFAULT 'Pending',

        task_date DATE,

        start_time TIME,

        end_time TIME,

        hours_spent DECIMAL(5,2),

        productivity_score INT DEFAULT 0,

        remarks TEXT,

        created_at TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- Categories ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories(

        category_id INT AUTO_INCREMENT PRIMARY KEY,

        category_name VARCHAR(50)
        UNIQUE NOT NULL
    )
    """)

    # Default Categories

    cursor.execute("""
    INSERT IGNORE INTO categories(category_name)
    VALUES
    ('Work'),
    ('Study'),
    ('Personal'),
    ('Health'),
    ('Fitness'),
    ('Learning'),
    ('Other')
    """)

    # ---------------- Daily Summary ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_summary(

        summary_id INT AUTO_INCREMENT PRIMARY KEY,

        summary_date DATE UNIQUE,

        total_tasks INT,

        completed_tasks INT,

        pending_tasks INT,

        total_hours DECIMAL(6,2),

        average_score DECIMAL(5,2)
    )
    """)

    conn.commit()

    cursor.close()
    conn.close()


# ==============================
# INSERT TASK
# ==============================

def add_task(data):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO tasks(

        task_name,
        category,
        priority,
        status,
        task_date,
        start_time,
        end_time,
        hours_spent,
        productivity_score,
        remarks

    )

    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, data)

    conn.commit()

    cursor.close()
    conn.close()


# ==============================
# FETCH ALL TASKS
# ==============================

def fetch_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT

    task_id,
    task_name,
    category,
    priority,
    status,
    task_date,
    start_time,
    end_time,
    hours_spent,
    productivity_score,
    remarks

    FROM tasks

    ORDER BY task_date DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# ==============================
# UPDATE TASK
# ==============================

def update_task(data):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    UPDATE tasks

    SET

    task_name=%s,
    category=%s,
    priority=%s,
    status=%s,
    task_date=%s,
    start_time=%s,
    end_time=%s,
    hours_spent=%s,
    productivity_score=%s,
    remarks=%s

    WHERE task_id=%s
    """

    cursor.execute(sql, data)

    conn.commit()

    cursor.close()
    conn.close()


# ==============================
# DELETE TASK
# ==============================

def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE task_id=%s",
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


# ==============================
# SEARCH TASK
# ==============================

def search_task(keyword):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM tasks

    WHERE

    task_name LIKE %s
    OR category LIKE %s
    OR status LIKE %s
    OR priority LIKE %s

    ORDER BY task_date DESC

    """, (

        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"

    ))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# ==============================
# FILTER CATEGORY
# ==============================

def filter_category(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM tasks

    WHERE category=%s

    ORDER BY task_date DESC

    """, (category,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# ==============================
# GET CATEGORIES
# ==============================

def get_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT category_name
    FROM categories
    ORDER BY category_name
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in rows]


# ==============================
# INITIALIZE DATABASE
# ==============================

def initialize_database():

    create_database()
    create_tables()