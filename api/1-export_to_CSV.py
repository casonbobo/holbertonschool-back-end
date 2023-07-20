#!/usr/bin/python3
"""
API set up to retrieve data from a url
"""
import requests
import csv

API_URL = "https://jsonplaceholder.typicode.com/users"
TODOS_URL = "https://jsonplaceholder.typicode.com/todos"


def get_employee_info(employee_id):
    # Get employee information from the API
    employee_response = requests.get(f"{API_URL}/{employee_id}")
    employee_data = employee_response.json()

    # Get TODO list for the employee
    todos_response = requests.get(TODOS_URL,
                                  params={"userId": employee_id})
    todos_data = todos_response.json()

    # Extract completed tasks and count
    completed_tasks = [todo["title"]
                       for todo in todos_data if todo["completed"]]
    num_completed_tasks = len(completed_tasks)
    total_tasks = len(todos_data)

    return (employee_data["name"],
            num_completed_tasks,
            total_tasks,
            completed_tasks)


def display_employee_progress(employee_name,
                              num_completed_tasks,
                              total_tasks,
                              completed_tasks):
    print(
        "Employee {} is done with tasks({}/{}):"
        .format(employee_name, num_completed_tasks, total_tasks)
    )
    for task in completed_tasks:
        print("\t", task)

def write_tasks_to_csv(employee_id, employee_name, tasks):
    file_name = f"{employee_id}.csv"
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])
        for task in tasks:
            writer.writerow([employee_id, employee_name, "Completed", task])


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <employee_id>")
        sys.exit(1)

    employee_id = int(sys.argv[1])
    try:
        name, completed, total, tasks = get_employee_info(employee_id)
        write_tasks_to_csv(employee_id, name, completed, total)
    except requests.exceptions.RequestException:
        print("Error: Unable to fetch data from the API.")
