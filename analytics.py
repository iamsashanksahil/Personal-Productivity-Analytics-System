from database import get_connection


# =====================================
# PRODUCTIVITY SCORE
# =====================================

def calculate_productivity_score(priority, status, hours):

    score = 0

    # Completion
    if status == "Completed":
        score += 50
    else:
        score += 10

    # Priority
    if priority == "High":
        score += 30
    elif priority == "Medium":
        score += 20
    else:
        score += 10

    # Hours Spent
    if hours <= 2:
        score += 20
    elif hours <= 5:
        score += 15
    else:
        score += 10

    return min(score, 100)


# =====================================
# TOTAL TASKS
# =====================================

def total_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


# =====================================
# COMPLETED TASKS
# =====================================

def completed_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status='Completed'
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


# =====================================
# PENDING TASKS
# =====================================

def pending_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM tasks
        WHERE status='Pending'
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


# =====================================
# COMPLETION RATE
# =====================================

def completion_rate():

    total = total_tasks()

    if total == 0:
        return 0

    completed = completed_tasks()

    return round((completed / total) * 100, 2)


# =====================================
# TOTAL HOURS
# =====================================

def total_hours():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT IFNULL(SUM(hours_spent),0)
        FROM tasks
    """)

    hours = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return float(hours)


# =====================================
# AVERAGE HOURS
# =====================================

def average_hours():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT IFNULL(AVG(hours_spent),0)
        FROM tasks
    """)

    avg = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return round(float(avg), 2)


# =====================================
# AVERAGE PRODUCTIVITY SCORE
# =====================================

def average_productivity():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT IFNULL(AVG(productivity_score),0)
        FROM tasks
    """)

    score = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return round(float(score), 2)


# =====================================
# MOST PRODUCTIVE CATEGORY
# =====================================

def most_productive_category():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            category,
            AVG(productivity_score)

        FROM tasks

        GROUP BY category

        ORDER BY AVG(productivity_score) DESC

        LIMIT 1

    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================
# LEAST PRODUCTIVE CATEGORY
# =====================================

def least_productive_category():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            category,
            AVG(productivity_score)

        FROM tasks

        GROUP BY category

        ORDER BY AVG(productivity_score)

        LIMIT 1

    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================
# HOURS BY CATEGORY
# =====================================

def hours_by_category():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            category,

            SUM(hours_spent)

        FROM tasks

        GROUP BY category

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# TASKS BY STATUS
# =====================================

def tasks_by_status():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            status,

            COUNT(*)

        FROM tasks

        GROUP BY status

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# TASKS BY PRIORITY
# =====================================

def tasks_by_priority():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            priority,

            COUNT(*)

        FROM tasks

        GROUP BY priority

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# TASKS BY CATEGORY
# =====================================

def tasks_by_category():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            category,

            COUNT(*)

        FROM tasks

        GROUP BY category

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# WEEKLY SUMMARY
# =====================================

def weekly_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            WEEK(task_date),

            COUNT(*),

            SUM(hours_spent),

            AVG(productivity_score)

        FROM tasks

        GROUP BY WEEK(task_date)

        ORDER BY WEEK(task_date)

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# MONTHLY SUMMARY
# =====================================

def monthly_summary():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            MONTHNAME(task_date),

            COUNT(*),

            SUM(hours_spent),

            AVG(productivity_score)

        FROM tasks

        GROUP BY MONTH(task_date)

        ORDER BY MONTH(task_date)

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# TOP 5 PRODUCTIVE TASKS
# =====================================

def top_productive_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            task_name,

            productivity_score

        FROM tasks

        ORDER BY productivity_score DESC

        LIMIT 5

    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# =====================================
# DASHBOARD DATA
# =====================================

def dashboard_data():

    return {

        "total_tasks": total_tasks(),

        "completed_tasks": completed_tasks(),

        "pending_tasks": pending_tasks(),

        "completion_rate": completion_rate(),

        "total_hours": total_hours(),

        "average_hours": average_hours(),

        "average_productivity": average_productivity(),

        "most_productive_category": most_productive_category(),

        "least_productive_category": least_productive_category()

    }