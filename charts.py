import matplotlib.pyplot as plt

from analytics import (
    tasks_by_status,
    tasks_by_category,
    tasks_by_priority,
    hours_by_category,
    weekly_summary,
    monthly_summary
)


# ============================================
# Completed vs Pending (Pie Chart)
# ============================================

def plot_task_status():

    data = tasks_by_status()

    if not data:
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.figure(figsize=(6,6))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Task Status Distribution")
    plt.show()


# ============================================
# Tasks by Category (Bar Chart)
# ============================================

def plot_tasks_by_category():

    data = tasks_by_category()

    if not data:
        return

    categories = [row[0] for row in data]
    count = [row[1] for row in data]

    plt.figure(figsize=(8,5))

    plt.bar(categories, count)

    plt.title("Tasks by Category")

    plt.xlabel("Category")

    plt.ylabel("Number of Tasks")

    plt.tight_layout()

    plt.show()


# ============================================
# Priority Distribution
# ============================================

def plot_priority_distribution():

    data = tasks_by_priority()

    if not data:
        return

    priority = [row[0] for row in data]
    count = [row[1] for row in data]

    plt.figure(figsize=(7,5))

    plt.bar(priority, count)

    plt.title("Task Priority Distribution")

    plt.xlabel("Priority")

    plt.ylabel("Tasks")

    plt.tight_layout()

    plt.show()


# ============================================
# Hours by Category
# ============================================

def plot_hours_by_category():

    data = hours_by_category()

    if not data:
        return

    category = [row[0] for row in data]
    hours = [float(row[1]) for row in data]

    plt.figure(figsize=(8,5))

    plt.bar(category, hours)

    plt.title("Hours Spent by Category")

    plt.xlabel("Category")

    plt.ylabel("Hours")

    plt.tight_layout()

    plt.show()


# ============================================
# Weekly Productivity Trend
# ============================================

def plot_weekly_productivity():

    data = weekly_summary()

    if not data:
        return

    weeks = [f"Week {row[0]}" for row in data]

    scores = [float(row[3]) for row in data]

    plt.figure(figsize=(8,5))

    plt.plot(
        weeks,
        scores,
        marker="o"
    )

    plt.title("Weekly Productivity Score")

    plt.xlabel("Week")

    plt.ylabel("Average Score")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ============================================
# Monthly Productivity Trend
# ============================================

def plot_monthly_productivity():

    data = monthly_summary()

    if not data:
        return

    months = [row[0] for row in data]

    scores = [float(row[3]) for row in data]

    plt.figure(figsize=(8,5))

    plt.plot(
        months,
        scores,
        marker="o"
    )

    plt.title("Monthly Productivity Score")

    plt.xlabel("Month")

    plt.ylabel("Average Score")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ============================================
# Monthly Hours Worked
# ============================================

def plot_monthly_hours():

    data = monthly_summary()

    if not data:
        return

    months = [row[0] for row in data]

    hours = [float(row[2]) for row in data]

    plt.figure(figsize=(8,5))

    plt.bar(
        months,
        hours
    )

    plt.title("Hours Worked Per Month")

    plt.xlabel("Month")

    plt.ylabel("Hours")

    plt.tight_layout()

    plt.show()


# ============================================
# Weekly Tasks Completed
# ============================================

def plot_weekly_tasks():

    data = weekly_summary()

    if not data:
        return

    weeks = [f"Week {row[0]}" for row in data]

    tasks = [row[1] for row in data]

    plt.figure(figsize=(8,5))

    plt.plot(
        weeks,
        tasks,
        marker="o"
    )

    plt.title("Tasks Completed Per Week")

    plt.xlabel("Week")

    plt.ylabel("Tasks")

    plt.grid(True)

    plt.tight_layout()

    plt.show()


# ============================================
# Display Every Chart
# ============================================

def show_all_charts():

    plot_task_status()

    plot_tasks_by_category()

    plot_priority_distribution()

    plot_hours_by_category()

    plot_weekly_productivity()

    plot_monthly_productivity()

    plot_monthly_hours()

    plot_weekly_tasks()