from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, Collapsible
from textual.containers import VerticalGroup, HorizontalGroup


class ToDoApp(App):
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalGroup(id='task_browser_VG'):
            for i in range(5):  # TODO: cycle through multiple times and populate based on database
                with HorizontalGroup():
                    yield Label("Task Title", classes="task_title_label")
                    yield Label(datetime.now().strftime("%H:%M:%S"), classes="task_timestamp_label")  # TODO: timestamp from database
                    yield Label("School", classes="category_label")  # TODO: category from database
        with Collapsible(id='task_info_collapsible'):
            pass
        yield Footer()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()