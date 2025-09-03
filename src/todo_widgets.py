import flet as ft

from todo_model import Task


class TaskWidget(ft.Column):
    def __init__(self, task: Task, on_status_change, on_delete, on_edit):
        super().__init__()
        self.task = task
        self.on_status_change = on_status_change
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.display_task = ft.Checkbox(
            value=task.completed, label=task.name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = str(self.task.name)
        self.display_view.visible = False
        self.edit_view.visible = True
        # self.update() removed

    def save_clicked(self, e):
        self.on_edit(self.task, self.edit_name.value)
        self.display_view.visible = True
        self.edit_view.visible = False
        # self.update() removed

    def status_changed(self, e):
        self.on_status_change(self.task, self.display_task.value)
        # self.update() removed

    def delete_clicked(self, e):
        self.on_delete(self.task)
