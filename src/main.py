from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer, ListView, ListItem, TextArea, Button, Input, OptionList
from textual.containers import HorizontalGroup, VerticalGroup
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


class AddWidget(VerticalGroup):
    def __init__(self, _DataManagement, _update_view):
        super().__init__()
        self._DataManagement = _DataManagement
        self._update_view = _update_view

    def compose(self) -> ComposeResult:
        yield Input(id="addwidget_task_input", placeholder="Task")
        yield Input(id="addwidget_desc_input", placeholder="Description")
        yield OptionList(id="category_optionlist")
        yield Button(id="addwidget_button", label="Add Task")

    def on_mount(self) -> None:
        # self.query_one("#category_optionlist", OptionList).add_options(self._DataManagement.)
        pass

    def on_button_pressed(self):
        self._DataManagement.add_task(str(self.query_one("#addwidget_task_input", Input).value),
                                      str(self.query_one("#addwidget_desc_input", Input).value),
                                      str(self.query_one("#category_optionlist", OptionList).OptionMessage),
                                      str(datetime.now()))
        self._update_view()

class ToDoApp(App):
    CSS_PATH = "main.tcss"

    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
        self._DataManagement = DataManagement("database.db")

    def compose(self) -> ComposeResult:
        yield Header()
        with HorizontalGroup():
            with VerticalGroup():
                yield ListView(id="tasks_listview")    
                yield AddWidget(self._DataManagement, self.update_view)
            yield TextArea(id="task_info_textarea", read_only=True)        
        yield Footer()
    
    def update_view(self) -> None:
        tasks_listview = self.query_one("#tasks_listview", ListView)
        textarea = self.query_one("#task_info_textarea", TextArea)

        tasks_listview.remove_children()
        textarea.load_text("")

        tasks = self._DataManagement.get_all_tasks()
        for task in tasks:
            tasks_listview.mount(TaskItem(task[1], task[2], task[3], task[4]))
        
        tasks_listview.action_cursor_down()

    def on_mount(self) -> None:
        self.update_view()

    def on_list_view_highlighted(self, event: ListView.Highlighted):
        tasks_listview = self.query_one("#tasks_listview", ListView)
        textarea = self.query_one("#task_info_textarea", TextArea)


        textarea.load_text(self._DataManagement.get_task_desc(event.item.task_name)[0][0])
        textarea.refresh()
    
    def on_key(self, event: events.Key) -> None:
       if event.key == "delete":
            task_name = self.query_one("#tasks_listview", ListView).highlighted_child.task_name
            self._DataManagement.remove_task(task_name)
            self.update_view()


if __name__ == "__main__":
    app = ToDoApp()
    app.run()