# app.py (Streamlit frontend)

import streamlit as st
import requests
import pandas as pd
import uuid

st.title("To-Do App")

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False
        self.deleted = False

def get_tasks():
    response = requests.get("http://localhost:8000/get_tasks/")
    tasks = response.json()

    data = []
    for task in tasks:
        data.append([task['title'], task['description'], task['completed'], task['deleted']])
        
    st.session_state['tasks_df'] = pd.DataFrame(data, columns=["title", "description", "completed", "deleted"])

def display_tasks():

    data_df = st.session_state['tasks_df']
    updated_df = st.data_editor(
        data_df,
        column_config={
            "completed": st.column_config.CheckboxColumn(
                "completed",
                help="Check if task is completed",
            ),
            "deleted": st.column_config.CheckboxColumn(
                "remove task",
                help="Check if task is to be removed",
            )
        },
        disabled=["widgets"],
        hide_index=False
    )

    # update tasks
    if st.button("Update Tasks"):
        for index, row in updated_df.iterrows():
            if row["deleted"]:
                response = requests.delete("http://localhost:8000/delete_task/", json={"title": row["title"], "description": row["description"]})
                if response.status_code == 200:
                    st.success("Task deleted successfully")
            else:
                response = requests.put("http://localhost:8000/update_task/", json={"title": row["title"], "description": row["description"],"completed": row["completed"]})
                if response.status_code == 200:
                    st.success("Task updated successfully")

        get_tasks()
    return updated_df


def main():
    st.header("Add Task")
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")
    
    if st.button("Add Task"):
        task = Task(title, description)
        response = requests.post("http://localhost:8000/add_task/", json=task.__dict__)
        if response.status_code == 200:
            st.success("Task added successfully")
    
    st.header("Tasks")

    get_tasks()
    display_tasks()

if __name__ == "__main__":
    main()
