"""
Project 3: To-Do List Manager
Features: add, view, delete, mark tasks as done, and save tasks in JSON.
Optional features included: tags and due dates.
Tasks remain saved after the program closes.
Run: python todo_list_manager.py
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    """Load tasks from JSON. Return an empty list if the file is missing."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Could not read saved tasks: {error}")
        return []


def save_tasks(tasks):
    """Save the current task list to JSON."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Could not save tasks: {error}")


def add_task(tasks):
    title = input("Enter task description: ").strip()
    if not title:
        print("Task description cannot be empty.")
        return

    tag = input("Enter tag (optional): ").strip()
    due_date = input("Enter due date (optional, e.g. 2026-12-01): ").strip()

    task = {
        "id": max((item.get("id", 0) for item in tasks), default=0) + 1,
        "title": title,
        "tag": tag,
        "due_date": due_date,
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully.")


def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n========== YOUR TASKS ==========")
    for task in tasks:
        status = "Done" if task.get("done") else "Pending"
        print(f"ID: {task['id']} | {task['title']} | {status}")
        if task.get("tag"):
            print(f"   Tag: {task['tag']}")
        if task.get("due_date"):
            print(f"   Due date: {task['due_date']}")


def find_task(tasks, task_id):
    return next((task for task in tasks if task.get("id") == task_id), None)


def read_task_id():
    try:
        return int(input("Enter task ID: "))
    except ValueError:
        print("Invalid ID. Please enter a whole number.")
        return None


def mark_task_done(tasks):
    view_tasks(tasks)
    task_id = read_task_id()
    if task_id is None:
        return

    task = find_task(tasks, task_id)
    if task is None:
        print("Task ID not found.")
        return

    task["done"] = True
    save_tasks(tasks)
    print("Task marked as done.")


def delete_task(tasks):
    view_tasks(tasks)
    task_id = read_task_id()
    if task_id is None:
        return

    task = find_task(tasks, task_id)
    if task is None:
        print("Task ID not found.")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted successfully.")


def main():
    tasks = load_tasks()

    while True:
        print("\n===== TO-DO LIST MANAGER =====")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_task_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Your tasks are saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    main()
