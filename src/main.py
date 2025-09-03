import flet as ft

from todo_service import TodoService
from todo_widgets import TaskWidget


class TodoApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.service = TodoService()
        self.new_task = ft.TextField(hint_text="Whats needs to be done?", expand=True)
        self.tasks_column = ft.Column()
        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )
        self.width = 600
        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks_column,
                ],
            ),
        ]
        self.refresh_tasks()

    def add_clicked(self, e):
        name = (self.new_task.value or "").strip()
        if name:
            self.service.add_task(name)
            self.new_task.value = ""
            self.refresh_tasks()
        self.update()

    def on_status_change(self, task, completed):
        self.service.set_task_completed(task, completed)
        self.refresh_tasks()
        self.update()

    def on_delete(self, task):
        self.service.delete_task(task)
        self.refresh_tasks()
        self.update()

    def on_edit(self, task, new_name):
        self.service.update_task_name(task, new_name)
        self.refresh_tasks()
        self.update()

    def refresh_tasks(self):
        status = (
            self.filter.tabs[self.filter.selected_index].text
            if self.filter.tabs[self.filter.selected_index].text
            else "all"
        )
        self.tasks_column.controls.clear()
        for task in self.service.get_tasks(str(status)):
            self.tasks_column.controls.append(
                TaskWidget(
                    task,
                    self.on_status_change,
                    self.on_delete,
                    self.on_edit,
                )
            )

    def tabs_changed(self, e):
        self.refresh_tasks()
        self.update()


def main(page: ft.Page):
    page.title = "To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    app = TodoApp()
    page.add(app)


ft.app(target=main)
