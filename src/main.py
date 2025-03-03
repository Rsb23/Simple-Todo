from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, ListView, ListItem, TextArea
from textual.containers import HorizontalGroup
from textual import events


class ToDoApp(App):
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with HorizontalGroup():
            yield ListView(id="tasks_listview")    
            yield TextArea(id="task_info_textarea", read_only=True)        
        yield Footer()
    
    def on_mount(self) -> None:
        tasks_listview = self.query_one("#tasks_listview", ListView)

        for i in range(5):
            tasks_listview.mount(ListItem(HorizontalGroup(
                Label("Task Title", classes="task_title_label"),
                Label("School", classes="category_label"),  # TODO: category from database
                Label(datetime.now().strftime("%H:%M:%S"), classes="task_timestamp_label"),  # TODO: timestamp from database
                classes="task_HG"
            )))

        tasks_listview.action_cursor_down()

    def on_list_view_highlighted(self):
        textarea = self.query_one("#task_info_textarea", TextArea)

        textarea.load_text("Test")
        textarea.refresh()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()