from datetime import datetime


# ==========================================
# VALIDATE TASK NAME
# ==========================================

def validate_task_name(task_name):

    if task_name.strip() == "":
        return False

    return True


# ==========================================
# VALIDATE HOURS
# ==========================================

def validate_hours(hours):

    try:

        value = float(hours)

        if value < 0:
            return False

        return True

    except ValueError:

        return False


# ==========================================
# VALIDATE DATE
# FORMAT : YYYY-MM-DD
# ==========================================

def validate_date(date):

    try:

        datetime.strptime(date, "%Y-%m-%d")

        return True

    except ValueError:

        return False


# ==========================================
# VALIDATE TIME
# FORMAT : HH:MM
# ==========================================

def validate_time(time):

    try:

        datetime.strptime(time, "%H:%M")

        return True

    except ValueError:

        return False


# ==========================================
# CALCULATE HOURS
# ==========================================

def calculate_hours(start_time, end_time):

    start = datetime.strptime(start_time, "%H:%M")

    end = datetime.strptime(end_time, "%H:%M")

    diff = end - start

    return round(diff.total_seconds() / 3600, 2)


# ==========================================
# PRODUCTIVITY SCORE
# ==========================================

def productivity_score(priority, status, hours):

    score = 0

    if status == "Completed":
        score += 50
    else:
        score += 10

    if priority == "High":
        score += 30

    elif priority == "Medium":
        score += 20

    else:
        score += 10

    if hours <= 2:
        score += 20

    elif hours <= 5:
        score += 15

    else:
        score += 10

    return min(score, 100)


# ==========================================
# FORMAT DATE
# ==========================================

def format_date(date):

    return datetime.strptime(
        date,
        "%Y-%m-%d"
    ).strftime("%d-%m-%Y")


# ==========================================
# FORMAT TIME
# ==========================================

def format_time(time):

    return datetime.strptime(
        time,
        "%H:%M"
    ).strftime("%I:%M %p")


# ==========================================
# CLEAR ENTRY WIDGETS
# ==========================================

def clear_entries(entries):

    for entry in entries:

        try:
            entry.delete(0, "end")

        except:
            pass


# ==========================================
# GET SELECTED ROW
# ==========================================

def selected_row(tree):

    selected = tree.focus()

    if selected == "":
        return None

    return tree.item(selected)["values"]


# ==========================================
# CURRENT DATE
# ==========================================

def current_date():

    return datetime.now().strftime("%Y-%m-%d")


# ==========================================
# CURRENT TIME
# ==========================================

def current_time():

    return datetime.now().strftime("%H:%M")