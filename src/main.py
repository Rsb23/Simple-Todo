from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, ListView, ListItem, TextArea
from textual.containers import HorizontalGroup
from textual import events

from database_parser import DataManagement


class TaskItem(ListItem):
    # https://github.com/Textualize/textual/discussions/1840
    CSS_PATH = "main.tcss"

    def __init__(self, task_name: str, desc: str, category: str, timestamp: str):
        super().__init__()
        self.task_name = task_name
        self.desc = desc
        self.category = category
        self.timestamp = timestamp
    
    def compose(self) -> ComposeResult:
        yield HorizontalGroup(
                Label(self.task_name, classes="task_title_label"),
                Label(self.category, classes="category_label"),
                Label(self.timestamp, classes="task_timestamp_label"),                        
                classes="task_HG"
        )

class ToDoApp(App):
    CSS_PATH = "main.tcss"

    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self._DataManagement = DataManagement("database.db")

    def compose(self) -> ComposeResult:
        yield Header()
        with HorizontalGroup():
            yield ListView(id="tasks_listview")    
            yield TextArea(id="task_info_textarea", read_only=True)        
        yield Footer()
    
    def on_mount(self) -> None:
        tasks_listview = self.query_one("#tasks_listview", ListView)

        tasks = self._DataManagement.get_all_tasks()
        for task in tasks:
            tasks_listview.mount(TaskItem(task[1], task[2], task[3], task[4]))

        tasks_listview.action_cursor_down()

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        tasks_listview = self.query_one("#tasks_listview", ListView)
        textarea = self.query_one("#task_info_textarea", TextArea)


        textarea.load_text(self._DataManagement.get_task_desc(event.item.task_name))
        textarea.refresh()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()