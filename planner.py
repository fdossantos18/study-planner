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



def load_tasks(file_path=TASKS_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            validate_tasks(tasks)
            return tasks
        
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


def get_task_summary(tasks):
    completed_count = 0 

    for task in tasks:
        status = task["completed"]
        if status:
            completed_count += 1


    return {
        "total": len(tasks),
        "completed": completed_count,
        "pending": len(tasks) - completed_count,
    }
        

def validate_tasks(tasks):
    if not isinstance(tasks, list):
        raise ValueError("Saved tasks must be a list.")

    seen_ids = set()

    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("Each saved task must be a dictionary.")

        for field in ("id", "title", "completed"):
            if field not in task:
                raise ValueError(f"Each saved task must include '{field}'.")


        if type(task["id"]) is not int or task["id"] <= 0:
            raise ValueError("Task IDs must be positive integers.")

        if task["id"] in seen_ids:
            raise ValueError(f"Duplicate task ID: {task['id']}.")

        seen_ids.add(task["id"])

        if not isinstance(task["title"], str):
            raise ValueError("Task titles must be strings.")

        if not task["title"].strip():
            raise ValueError("Task titles must not be blank.")

        if type(task["completed"]) is not bool:
            raise ValueError("Task completion must be True or False.")

    




