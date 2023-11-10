# Todo backend app with fastAPI
from fastapi import FastAPI
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False
    deleted: bool = False


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        return self.tasks

    def update_task(self, task: Task):
        for index, t in enumerate(self.tasks):
            if t.title == task.title:
                t = task
                break
                
    def delete_task(self, task: Task):
        for index, t in enumerate(self.tasks):
            if t.title == task.title:
                self.tasks.pop(index)
                break

app = FastAPI()

task_manager = TaskManager()

@app.post("/add_task/")
def add_task(task: Task):
    task_manager.add_task(task)
    return {"message": "Task added successfully"}

@app.get("/get_tasks/")
def get_tasks() -> list[Task]:
    return task_manager.get_tasks()

@app.put("/update_task/")
def update_task(task: Task):
    task_manager.update_task(task)
    return {"message": "Task updated successfully"}

@app.delete("/delete_task/")
def delete_task(task: Task):
    task_manager.delete_task(task)
    return {"message": "Task deleted successfully"}