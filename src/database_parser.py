from datetime import datetime

import sqlite3
from sqlite3 import Error


class DataManagement():
    def __init__(self, filepath):
        self.conn = self.create_connection(filepath)
        self.create_tables()

    def create_connection(self, filepath) -> sqlite3.Connection | ConnectionAbortedError:
        try:
            return sqlite3.connect(filepath)
        except Error as e:
            return ConnectionAbortedError(e)
    
    def create_tables(self) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    name text NOT NULL,
                    desc text NOT NULL,
                    category text NOT NULL,
                    creation_date DATE
                );
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    category_name text NOT NULL
                );
                """
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e
    
    def add_task(self, name: str, desc: str, category: str, creation_date: str) -> None:
        # https://www.sqlitetutorial.net/sqlite-python/insert/
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO tasks(name,desc,category,creation_date)
                VALUES(?,?,?,?)
                """,
                (name, desc, category, creation_date)
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
    
    def add_category(self, category_name: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"""
                INSERT INTO categories(category_name)
                VALUES(?)
                """,
                (category_name,)
            )
            self.conn.commit()
        
        except sqlite3.OperationalError as e:
            raise e
        
    def remove_task(self, category_name: str) -> None:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                DELETE FROM categories WHERE category_name = ?
                """,
                (category_name,)
            )
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise e
    
    def get_all_categories(self) -> tuple:
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT category_name FROM categories")
            rows = cursor.fetchall()

            data = []
            for row in rows:
                data.append(row[0])
            return data
        except sqlite3.OperationalError as e:
            raise e