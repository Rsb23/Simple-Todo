from datetime import datetime

import sqlite3
from sqlite3 import Error


class DataManagement():
    def __init__(self, filepath):
        self.conn = self.create_connection(filepath)
        self.create_table()  # creates table if none exists

    def create_connection(self, filepath) -> sqlite3.Connection | ConnectionAbortedError:
        try:
            return sqlite3.connect(filepath)
        except Error as e:
            return ConnectionAbortedError(e)
    
    def create_table(self) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    name text NOT NULL,
                    desc text NOT NULL,
                    creation_date DATE
                );
                """
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e
    
    def add_task(self, task: tuple) -> None:
        # https://www.sqlitetutorial.net/sqlite-python/insert/
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO tasks(name,desc,creation_date)
                VALUES(?,?,?)
                """,
                task
            )
            self.conn.commit()
        
        except sqlite3.OperationalError as e:
            raise e
    
    def remove_task(self, name: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                DELETE FROM tasks WHERE name = ?
                """,
                (name,)
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e

    def update_task_name(self, target_name: str, name: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE tasks SET name = ? WHERE name = ?
                """,
                (name, target_name)
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e

    def update_task_desc(self, target_name: str, desc: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                UPDATE tasks SET desc = ? WHERE name = ?
                """,
                (desc, target_name)
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e

    def get_all_tasks(self) -> tuple:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            rows = cursor.fetchall()
            return tuple(rows)
        except sqlite3.OperationalError as e:
            raise e
    
    def get_task_desc(self, name: str) -> str:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT desc FROM tasks WHERE name = ?", (name,))
            desc = cursor.fetchall()
            return tuple(desc)
        except sqlite3.OperationalError as e:
            raise e