from todo_model import Task


class TodoService:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, name: str) -> Task:
        task = Task(name=name)
        self.tasks.append(task)
        return task

    def delete_task(self, task: Task):
        self.tasks.remove(task)

    def update_task_name(self, task: Task, new_name: str):
        task.name = new_name

    def set_task_completed(self, task: Task, completed: bool):
        task.completed = completed

    def get_tasks(self, status: str = "all") -> list[Task]:
        if status == "all":
            return self.tasks
        elif status == "active":
            return [t for t in self.tasks if not t.completed]
        elif status == "completed":
            return [t for t in self.tasks if t.completed]
        return self.tasks
