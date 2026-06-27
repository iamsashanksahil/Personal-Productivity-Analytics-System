import os
from datetime import datetime

import pandas as pd
from tkinter import messagebox

from database import get_connection


# ==========================================
# CREATE REPORTS FOLDER
# ==========================================

REPORT_FOLDER = "reports"

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


# ==========================================
# LOAD DATA FROM MYSQL
# ==========================================

def fetch_dataframe():

    conn = get_connection()

    query = """
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
            remarks,
            created_at

        FROM tasks

        ORDER BY task_date DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==========================================
# EXPORT CSV
# ==========================================

def export_csv():

    try:

        df = fetch_dataframe()

        if df.empty:

            messagebox.showinfo(
                "Export",
                "No records found."
            )

            return

        filename = os.path.join(

            REPORT_FOLDER,

            f"Productivity_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        )

        df.to_csv(

            filename,

            index=False

        )

        messagebox.showinfo(

            "Success",

            f"CSV exported successfully.\n\n{filename}"

        )

    except Exception as e:

        messagebox.showerror(

            "Export Error",

            str(e)

        )


# ==========================================
# EXPORT EXCEL
# ==========================================

def export_excel():

    try:

        df = fetch_dataframe()

        if df.empty:

            messagebox.showinfo(

                "Export",

                "No records found."

            )

            return

        filename = os.path.join(

            REPORT_FOLDER,

            f"Productivity_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        )

        with pd.ExcelWriter(

            filename,

            engine="openpyxl"

        ) as writer:

            df.to_excel(

                writer,

                sheet_name="Tasks",

                index=False

            )

        messagebox.showinfo(

            "Success",

            f"Excel exported successfully.\n\n{filename}"

        )

    except Exception as e:

        messagebox.showerror(

            "Export Error",

            str(e)

        )


# ==========================================
# EXPORT DAILY SUMMARY
# ==========================================

def export_daily_summary():

    try:

        conn = get_connection()

        query = """

            SELECT

                task_date,

                COUNT(*) AS total_tasks,

                SUM(status='Completed') AS completed_tasks,

                SUM(status='Pending') AS pending_tasks,

                SUM(hours_spent) AS total_hours,

                AVG(productivity_score) AS average_score

            FROM tasks

            GROUP BY task_date

            ORDER BY task_date

        """

        df = pd.read_sql(query, conn)

        conn.close()

        filename = os.path.join(

            REPORT_FOLDER,

            f"Daily_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        )

        df.to_excel(

            filename,

            index=False

        )

        messagebox.showinfo(

            "Success",

            f"Daily Summary exported.\n\n{filename}"

        )

    except Exception as e:

        messagebox.showerror(

            "Export Error",

            str(e)

        )


# ==========================================
# EXPORT CATEGORY SUMMARY
# ==========================================

def export_category_summary():

    try:

        conn = get_connection()

        query = """

            SELECT

                category,

                COUNT(*) AS total_tasks,

                SUM(hours_spent) AS total_hours,

                AVG(productivity_score) AS average_score

            FROM tasks

            GROUP BY category

            ORDER BY category

        """

        df = pd.read_sql(query, conn)

        conn.close()

        filename = os.path.join(

            REPORT_FOLDER,

            f"Category_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        )

        df.to_excel(

            filename,

            index=False

        )

        messagebox.showinfo(

            "Success",

            f"Category Summary exported.\n\n{filename}"

        )

    except Exception as e:

        messagebox.showerror(

            "Export Error",

            str(e)

        )