import json 
import tkinter as tk 
from tkinter import ttk, simpledialog, messagebox
from planner import (
    load_tasks, 
    add_task, 
    save_tasks, 
    complete_task,
    filter_tasks,
    search_tasks,
    set_task_completed,
    rename_task,
    undo_status_change, 
    get_task_summary, 
    sort_tasks_by_title,
)

def main():
    # creates the new application
    window = tk.Tk()
    # sets the title bar text
    window.title("Study Planner")
    # sets its initial width and height in pixels
    window.geometry("500x550")

    # creates a text element inside window
    heading = ttk.Label(window, text="My Study Planner")
    # places that element in the window; pady=20 adds vertical space around it
    heading.pack(pady=20)

    progress_label = ttk.Label(window, text="")
    progress_label.pack(pady=5)

    status_label = ttk.Label(window, text="")
    status_label.pack(pady=5)

    title_entry = ttk.Entry(window, width=40)
    title_entry.pack(padx=20, pady=5)

    def on_add_task():
        nonlocal next_task_id

        title = title_entry.get().strip()

        if not title:
            status_label.config(text="Please enter a title.")
            return 

        # print(f"You entered: {title}")
        add_task(tasks, next_task_id, title)
        next_task_id += 1
        save_tasks(tasks)
        refresh_task_list()

        title_entry.delete(0, tk.END)
        status_label.config(text="Task added!")


    add_button = ttk.Button(
        window, 
        text="Add Task",
        command=on_add_task,
    )
    add_button.pack(pady=5)

    try:
        tasks = load_tasks()

    except json.JSONDecodeError:
        messagebox.showerror(
            "Could not load tasks",
            "The study_tasks.json file contains invalid JSON.\n\n"
            "Your saved file has not been changed. "
            "Correct the file before reopening the planner.",
            parent=window,
        )
        window.destroy()
        return 


    except ValueError as error:
        messagebox.showerror(
            "Invalid saved tasks",
            f"The saved task data is invalid:\n{error}\n\n"
            "Your saved file has not been changed. "
            "Correct the file before reopening the planner.",
            parent=window,
        )
        window.destroy()
        return

    undo_stack = []
    visible_tasks = []
    next_task_id = max((task["id"] for task in tasks), default=0) + 1

    filter_var = tk.StringVar(value="All")

    filter_dropdown = ttk.Combobox(
        window, 
        textvariable=filter_var,
        values=("All", "Pending", "Completed"),
        state="readonly",
    )
    filter_dropdown.pack(pady=5)


    # Search tasks
    search_label = ttk.Label(window, text="Search titles (press Enter):")
    search_label.pack(pady=5)

    search_entry = ttk.Entry(window, width=40)
    search_entry.pack(padx=20, pady=5)


    # Sort Dropdown
    sort_var = tk.StringVar(value="Original order")

    sort_dropdown = ttk.Combobox(
        window,
        textvariable=sort_var,
        values=("Original order", "Title A-Z"),
        state="readonly",
    )
    sort_dropdown.pack(pady=5)

    # Listbox
    task_list = tk.Listbox(window, width=60, height=10)
    task_list.pack(padx=20, pady=10, fill="both", expand=True)

    def refresh_task_list():
        nonlocal visible_tasks

        summary = get_task_summary(tasks)

        progress_label.config(
            text=f"{summary['completed']} of {summary['total']} tasks completed"
        )

        selected_filter = filter_var.get()

        if selected_filter == "All":
            visible_tasks = tasks.copy()
        elif selected_filter == "Pending":
            visible_tasks = filter_tasks(tasks, False)
        else:
            visible_tasks = filter_tasks(tasks, True)

        query = search_entry.get()
        visible_tasks = search_tasks(visible_tasks, query) 

        if sort_var.get() == "Title A-Z":
            visible_tasks = sort_tasks_by_title(visible_tasks)

        task_list.delete(0, tk.END)

        for task in visible_tasks:
            task_id = task["id"]
            title = task["title"]
            is_completed = task["completed"]

            
            if is_completed:
                status_text = "[Completed]"
            else:
                status_text = "[Pending]"

            task_list.insert(tk.END, f'{task_id}. {title} {status_text}')


    # search 
    def on_search(event):
        refresh_task_list()

    search_entry.bind("<Return>", on_search)


    # filter changed 
    def on_filter_changed(event):
        refresh_task_list()

    filter_dropdown.bind("<<ComboboxSelected>>", on_filter_changed)


    def on_complete_task():
        selection = task_list.curselection()

        if not selection:
            status_label.config(text="Please select a task.")
            return 

        selected_index = selection[0]
        selected_task = visible_tasks[selected_index]

        if selected_task["completed"]:
            status_label.config(text="Task is already completed.")
            return 

        change = {
            "task_id": selected_task["id"],
            "previous_completed": selected_task["completed"],
        }

        if complete_task(tasks, selected_task["id"]):
            undo_stack.append(change)
            save_tasks(tasks)
            refresh_task_list()
            status_label.config(text="Task completed!")

        
    # Create button 
    complete_button = ttk.Button(
        window, 
        text="Complete Selected",
        command=on_complete_task,
    )
    complete_button.pack(pady=5)

    def on_mark_pending():
        selection = task_list.curselection()

        if not selection:
            status_label.config(text="Please select a task.")
            return 

        selected_index = selection[0]
        selected_task = visible_tasks[selected_index]

        if not selected_task["completed"]:
            status_label.config(text="Task is already pending.")
            return 

        change = {
            "task_id": selected_task["id"],
            "previous_completed": selected_task["completed"],
        }

        if set_task_completed(tasks, selected_task["id"], False):
            undo_stack.append(change)
            save_tasks(tasks)
            refresh_task_list()
            status_label.config(text="Task marked pending!")


    # Create button -> mark pending 
    pending_button = ttk.Button(
        window,
        text="Mark Pending",
        command=on_mark_pending,
    )
    pending_button.pack(pady=5)


    def on_rename_task():
        selection = task_list.curselection()

        if not selection:
            status_label.config(text="Please select a task.")
            return 

        selected_task = visible_tasks[selection[0]]

        new_title = simpledialog.askstring(
            "Rename task",
            "Enter the new title:",
            initialvalue=selected_task["title"],
            parent=window, 
        )

        if new_title is None:
            return 

        new_title = new_title.strip()

        if not new_title:
            status_label.config(text="Please enter a title.")
            return 

        if rename_task(tasks, selected_task["id"], new_title):
            save_tasks(tasks)
            refresh_task_list()
            status_label.config(text="Task renamed!")


    # Create rename button
    rename_button = ttk.Button(
        window,
        text="Rename Selected",
        command=on_rename_task,
    )
    rename_button.pack(pady=5)


    def on_undo_status():
        if not undo_stack:
            status_label.config(text="No status changes to undo.")
            return 

        if undo_status_change(tasks, undo_stack):
            save_tasks(tasks)
            refresh_task_list()
            status_label.config(text="Last status change undone.")
            
        else:
            status_label.config(text="Could not find the task to undo.")


    # Create Undo button
    undo_button = ttk.Button(
        window,
        text="Undo Status Change",
        command=on_undo_status,
    )
    undo_button.pack(pady=5)


    def on_sort_changed(event):
        refresh_task_list()
    
    sort_dropdown.bind("<<ComboboxSelected>>", on_sort_changed)




    refresh_task_list()
    # starts the event loop, which processes clicks, keyboard input, and window events
    window.mainloop()


if __name__ == "__main__":
    main()



