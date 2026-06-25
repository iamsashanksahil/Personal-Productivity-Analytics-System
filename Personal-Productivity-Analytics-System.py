#shows error, working on it, its pending yet
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "productivity_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

class ProductivityApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Personal Productivity Analytics System")
        self.root.geometry("1000x600")

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):

        tk.Label(self.root, text="Task Name").grid(row=0, column=0, padx=10, pady=10)

        self.task_entry = tk.Entry(self.root, width=30)
        self.task_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Category").grid(row=0, column=2)

        self.category_combo = ttk.Combobox(
            self.root,
            values=["Work", "Study", "Personal"]
        )
        self.category_combo.grid(row=0, column=3)

        tk.Label(self.root, text="Priority").grid(row=1, column=0)

        self.priority_combo = ttk.Combobox(
            self.root,
            values=["High", "Medium", "Low"]
        )
        self.priority_combo.grid(row=1, column=1)

        tk.Label(self.root, text="Status").grid(row=1, column=2)

        self.status_combo = ttk.Combobox(
            self.root,
            values=["Pending", "Completed"]
        ) 
        self.status_combo.grid(row=1, column=3)

        tk.Label(self.root, text="Hours Spent").grid(row=2, column=0)

        self.hours_entry = tk.Entry(self.root)
        self.hours_entry.grid(row=2, column=1)

        tk.Button( 
            self.root,
            text="Add Task",
            command=self.add_task
        ).grid(row=3, column=0, pady=15)

        tk.Button(
            self.root,
            text="Delete Task",
            command=self.delete_task
        ).grid(row=3, column=1)

        tk.Button(
            self.root,
            text="Refresh",
            command=self.load_tasks
        ).grid(row=3, column=2)

        tk.Button( 
            self.root,
            text="Analytics",
            command=self.analytics
        ).grid(row=3, column=3)

        columns = (
            "ID",
            "Task",
            "Category",
            "Priority",
            "Status",
            "Hours"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.grid(
            row=4,
            column=0,
            columnspan=6,
            padx=10,
            pady=20,
            sticky="nsew"
        )

    def add_task(self):

        task = self.task_entry.get()
        category = self.category_combo.get()
        priority = self.priority_combo.get()
        status = self.status_combo.get()

        try:
            hours = float(self.hours_entry.get())
        except:
            messagebox.showerror(
                "Error",
                "Enter valid hours."
            )
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tasks
            (
                task_name,
                category,
                priority,
                status,
                hours_spent
            )
            VALUES
            (%s,%s,%s,%s,%s)
            """,
            (
                task,
                category,
                priority,
                status,
                hours
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        self.load_tasks()

    def load_tasks(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
            task_id,
            task_name,
            category,
            priority,
            status,
            hours_spent
            FROM tasks
            """
        )

        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert(
                "",
                "end",
                values=row
            )

        cursor.close()
        conn.close()

    def delete_task(self):

        selected = self.tree.focus()

        if not selected:
            return

        task_id = self.tree.item(
            selected
        )["values"][0]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE task_id=%s
            """,
            (task_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        self.load_tasks()

    def analytics(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            """
        )
        total_tasks = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE status='Completed'
            """
        )
        completed = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tasks
            WHERE status='Pending'
            """
        )
        pending = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT IFNULL(
                SUM(hours_spent),
                0
            )
            FROM tasks
            """
        )
        total_hours = cursor.fetchone()[0]

        completion_rate = 0

        if total_tasks > 0:
            completion_rate = round(
                completed * 100 / total_tasks,
                2
            )

        cursor.close()
        conn.close()

        messagebox.showinfo(
            "Productivity Analytics",
            f"""
Total Tasks : {total_tasks}

Completed Tasks : {completed}

Pending Tasks : {pending}

Completion Rate : {completion_rate}%

Total Hours Worked : {total_hours}
"""
        )

root = tk.Tk()

app = ProductivityApp(root)

root.mainloop()
