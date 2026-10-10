import tkinter as tk 
from tkinter import ttk, simpledialog
from planner import load_tasks, add_task, save_tasks, complete_task, filter_tasks, search_tasks, set_task_completed, rename_task


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

    tasks = load_tasks()
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


    # Listbox
    task_list = tk.Listbox(window, width=60, height=10)
    task_list.pack(padx=20, pady=10, fill="both", expand=True)

    def refresh_task_list():
        nonlocal visible_tasks

        selected_filter = filter_var.get()

        if selected_filter == "All":
            visible_tasks = tasks.copy()
        elif selected_filter == "Pending":
            visible_tasks = filter_tasks(tasks, False)
        else:
            visible_tasks = filter_tasks(tasks, True)

        query = search_entry.get()
        visible_tasks = search_tasks(visible_tasks, query) 

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

        if complete_task(tasks, selected_task["id"]):
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

        if set_task_completed(tasks, selected_task["id"], False):
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


    refresh_task_list()
    # starts the event loop, which processes clicks, keyboard input, and window events
    window.mainloop()


if __name__ == "__main__":
    main()



