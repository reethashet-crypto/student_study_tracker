import csv
import os

FILE = "tasks.csv"

def load_tasks():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_tasks(tasks):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["subject", "task", "status"]
        )
        writer.writeheader()
        writer.writerows(tasks)


def add_task():
    subject = input("Enter subject: ")
    task = input("Enter study task: ")

    tasks = load_tasks()
    tasks.append({
        "subject": subject,
        "task": task,
        "status": "Pending"
    })

    save_tasks(tasks)
    print("Task added successfully!")


def view_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    for i, task in enumerate(tasks, start=1):
        print(
            f"{i}. {task['subject']} - "
            f"{task['task']} - {task['status']}"
        )


def complete_task():
    tasks = load_tasks()
    view_tasks()

    if not tasks:
        return

    try:
        number = int(input("Enter task number: "))

        if 1 <= number <= len(tasks):
            tasks[number - 1]["status"] = "Completed"
            save_tasks(tasks)
            print("Task completed!")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


while True:
    print("\n===== STUDY TRACKER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        complete_task()
    elif choice == "4":
        break
    else:
        print("Invalid choice.")