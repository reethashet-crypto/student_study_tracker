import csv
from datetime import datetime, date

FILE_NAME = "tasks.csv"

# Load tasks from CSV file
def load_tasks():
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            tasks = []

            for row in reader:
                tasks.append({
                    "subject": row.get("subject", ""),
                    "task": row.get("task", ""),
                    "status": row.get("status", "Pending") or "Pending",
                    "deadline": row.get("deadline", "") or ""
                })

            return tasks

    except FileNotFoundError:
        return []


# Save tasks to CSV file
def save_tasks(tasks):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        fields = ["subject", "task", "status", "deadline"]
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(tasks)


# Add a new task
def add_task():
    tasks = load_tasks()

    subject = input("Enter subject: ")
    task = input("Enter task: ")

    while True:
        deadline = input("Enter deadline (DD-MM-YYYY), or press Enter to skip: ").strip()

        if deadline == "":
            break

        try:
            datetime.strptime(deadline, "%d-%m-%Y")
            break
        except ValueError:
            print("Invalid date! Please use DD-MM-YYYY.")

    tasks.append({
        "subject": subject,
        "task": task,
        "status": "Pending",
        "deadline": deadline
    })

    save_tasks(tasks)
    print("Task added successfully!")


# View all tasks
def view_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    print("\n------ YOUR TASKS ------")

    for i, task in enumerate(tasks, start=1):
        deadline = task["deadline"] if task["deadline"] else "Not set"

        print(f"\n{i}. Subject: {task['subject']}")
        print(f"   Task: {task['task']}")
        print(f"   Status: {task['status']}")
        print(f"   Deadline: {deadline}")


# Mark a task as completed
def complete_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    view_tasks()

    try:
        number = int(input("\nEnter task number to complete: "))

        if 1 <= number <= len(tasks):
            tasks[number - 1]["status"] = "Completed"
            save_tasks(tasks)
            print("Task marked as completed!")
        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")


# View study progress
def view_progress():
    tasks = load_tasks()

    total = len(tasks)
    completed = sum(1 for task in tasks if task["status"] == "Completed")
    pending = total - completed

    if total == 0:
        print("No tasks available.")
        return

    percentage = (completed / total) * 100

    print("\n------ STUDY PROGRESS ------")
    print("Total tasks:", total)
    print("Completed tasks:", completed)
    print("Pending tasks:", pending)
    print(f"Completion: {percentage:.1f}%")


# View deadlines
def view_deadlines():
    tasks = load_tasks()
    today = date.today()
    deadline_tasks = []

    for task in tasks:
        if task["deadline"]:
            due_date = datetime.strptime(
                task["deadline"], "%d-%m-%Y"
            ).date()

            deadline_tasks.append((due_date, task))

    if not deadline_tasks:
        print("No deadlines available.")
        return

    deadline_tasks.sort(key=lambda item: item[0])

    print("\n------ DEADLINE TRACKER ------")

    for due_date, task in deadline_tasks:

        if task["status"] == "Completed":
            label = "COMPLETED"
        elif due_date < today:
            label = "OVERDUE"
        elif due_date == today:
            label = "DUE TODAY"
        else:
            label = "UPCOMING"

        print(f"\nSubject: {task['subject']}")
        print(f"Task: {task['task']}")
        print(f"Deadline: {due_date.strftime('%d-%m-%Y')}")
        print("Status:", label)


def update_deadline():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    view_tasks()

    try:
        number = int(input("\nEnter the task number to update its deadline: "))

        if 1 <= number <= len(tasks):

            while True:
                deadline = input("Enter new deadline (DD-MM-YYYY): ")

                try:
                    datetime.strptime(deadline, "%d-%m-%Y")
                    break
                except ValueError:
                    print("Invalid date! Please use DD-MM-YYYY.")

            tasks[number - 1]["deadline"] = deadline
            save_tasks(tasks)

            print("Deadline updated successfully!")

        else:
            print("Invalid task number.")

    except ValueError:
        print("Please enter a valid number.")
# Main menu
while True:
    print("\n====== STUDENT STUDY TRACKER ======")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. View Progress")
    print("5. View Deadlines")
    print("6. Update Deadline")
    print("7.Exit")
    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        view_tasks()

    elif choice == "3":
        complete_task()

    elif choice == "4":
        view_progress()

    elif choice == "5":
        view_deadlines()

    elif choice == "6":
        update_deadline()

    elif choice=="7":
        print("Thank you for using Study Tracker!!!")
        break
        
        
