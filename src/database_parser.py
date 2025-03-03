from datetime import datetime

import sqlite3
from sqlite3 import Error


class DataManagement():
    def __init__(self):
        self.conn = self.create_connection("database.db")

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
    
    def remove_task(self, id: int) -> bool:
        pass

    def update_task_name(self, name: str) -> bool:
        pass

    def update_task_desc(self, desc: str) -> bool:
        pass


_DataManagement = DataManagement()
_DataManagement.create_table()
_DataManagement.add_task(("First Task", "This is a test description", datetime.now()))
_DataManagement.add_task(("Second Task", "This is a test description", datetime.now()))
_DataManagement.add_task(("Third Task", "This is a test description", datetime.now()))