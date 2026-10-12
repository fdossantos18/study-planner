import json 
from pathlib import Path 

TASKS_FILE = Path(__file__).with_name("study_tasks.json")


def add_task(tasks, task_id, title):
    """
    This adds a task to a list (tasks) as a dictionary 
    """
    task = {
        "id": task_id,
        "title": title,
        "completed": False 
    }

    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    return set_task_completed(tasks, task_id, True)

    

def set_task_completed(tasks, task_id, completed):

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = completed 
            return True 

    return False 



def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)



def load_tasks():
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
        
    except FileNotFoundError:
        return []
        

def filter_tasks(tasks, completed):
    filtered = []

    for task in tasks:
        status = task["completed"]
        if status == completed:
            filtered.append(task)

    return filtered 


def search_tasks(tasks, query):
    matches = []
    query = query.strip().casefold()

    for task in tasks:
        if query in task["title"].casefold():
            matches.append(task) 


    return matches 


def rename_task(tasks, task_id, new_title):

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            return True 

    return False 


def undo_status_change(tasks, undo_stack):
    if not undo_stack:
        return False 

    last_change = undo_stack[-1]

    restored = set_task_completed(
        tasks, 
        last_change["task_id"],
        last_change["previous_completed"],
    )

    if restored:
        undo_stack.pop()
        return True 
    
    
    return False 
        

        




