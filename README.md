# Study Planner

A Python study planner built step by step to organize study tasks labeled by status.

## Features

- Add and rename study tasks.
- Mark tasks completed or pending.
- Filter tasks by completion status.
- Search task titles without case sensitivity.
- Save tasks locally in JSON.
- Use a desktop interface or a simpler terminal interface.

## Requirements

Python 3 with Tkinter available for the desktop interface.

## Run the app

From the project folder:

```bash
python gui.py
```

For the terminal interface:

```bash
python cli.py
```

## Run tests

```bash
python -m unittest -v
```

## Project structure

- `planner.py`: task operations and JSON persistence.
- `gui.py`: Tkinter desktop interface.
- `cli.py`: terminal interface.
- `test_planner.py`: automated tests.

Personal tasks are stored in `study_tasks.json`, which is excluded from Git.
The app starts with an empty list when that file does not exist.

## What I am learning

- Lists, dictionaries, and shared references.
- Linear search and filtering.
- Separating application logic from interface code.
- Event-driven programming with callbacks.
- Automated testing.
- Git branches, commits, and pull requests.