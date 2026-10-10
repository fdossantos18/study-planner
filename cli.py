
from planner import ( # type: ignore
    add_task,
    complete_task,
    filter_tasks,
    load_tasks,
    save_tasks,
)

def list_tasks(tasks, empty_message="No tasks yet. "):
    if not tasks:
        print(empty_message)
        return 
    
    
    for task in tasks:
        task_id = task["id"]
        title = task["title"]
        is_completed = task["completed"]

        
        if is_completed:
            status_label = "[Completed]"
        else:
            status_label = "[Pending]"

        print(f"{task_id}. {title} {status_label}")



def main():
    tasks = load_tasks()
    next_task_id = max((task["id"] for task in tasks), default=0) + 1


    while True:
        print("\nStudy Planner")
        print("1. Add a task")
        print("2. List tasks")
        print("3. Complete a task")
        print("4. Exit")

        choice = input("Choose an option: ")

        # Add a task
        if choice == "1":
            title = input("what would you like to study? ").strip()

            if not title:
                print("Please enter a title.")
                continue 

            add_task(tasks, next_task_id, title)

            next_task_id += 1

            # save it after adding a task 
            save_tasks(tasks)
            print("Task added!")

        # List Tasks 
        elif choice == "2":
            print("1. All tasks")
            print("2. Pending tasks")
            print("3. Completed tasks")

            filter_choice = input("Which tasks would you like to see? ").strip()

            if filter_choice == "1":
                list_tasks(tasks)

            elif filter_choice == "2":
                pending_tasks = filter_tasks(tasks, False)
                list_tasks(pending_tasks, empty_message="No pending tasks.")
                
            elif filter_choice == "3":
                completed_tasks = filter_tasks(tasks, True)
                list_tasks(completed_tasks, empty_message="No completed tasks.")

            else:
                print("Invalid filter option.")


        # Complete a task
        elif choice == "3":
            try:
                task_id = int(input("Enter the task ID: "))
            except ValueError:
                print("Please enter a whole number.")
                continue 

            if complete_task(tasks, task_id):
                save_tasks(tasks)
                print("Task completed!")
            else:
                print("Task not found.")
            
        # Exit program
        elif choice == "4":
            save_tasks(tasks)
            print("Goodbye!")
            break  
        else:
            print("Invalid option. Try again.")



if __name__ == "__main__":
    main()


