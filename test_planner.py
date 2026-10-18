import unittest

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import gui
from planner import (
    rename_task,
    set_task_completed,
    filter_tasks,
    search_tasks,
    undo_status_change,
    get_task_summary,
    load_tasks,
    validate_tasks,
    sort_tasks_by_title,
    save_tasks,
)


class PlannerTests(unittest.TestCase):
    
    def test_rename_preserves_other_fields(self):
        tasks = [
            {"id": 7, "title": "Practce graphs", "completed": True},
        ]

        result = rename_task(tasks, 7, "Practice graphs")

        self.assertTrue(result)
        self.assertEqual(
            tasks[0],
            {"id": 7, "title": "Practice graphs", "completed": True},
        )


    def test_set_task_completed(self):
        tasks = [
            {"id": 9, "title": "Big O", "completed": False},
        ] 

        result = set_task_completed(tasks, 9, True)

        self.assertTrue(result)
        self.assertEqual(
            tasks[0],
            {"id": 9, "title": "Big O", "completed": True},
        )


    def test_rename_missing_id_leaves_tasks_unchanged(self):
        tasks = [
            {"id": 7, "title": "Practice graphs", "completed": True},
        ]

        result = rename_task(tasks, 999, "Binary search")

        self.assertFalse(result)
        self.assertEqual(
            tasks, 
            [{"id": 7, "title": "Practice graphs", "completed": True}]
        )


    def test_search_within_pending_tasks(self):
        tasks = [
            {"id": 1, "title": "Practice graphs", "completed": False},
            {"id": 2, "title": "Review graphs", "completed": True},
            {"id": 3, "title": "Binary search", "completed": False},
        ]

        pending_tasks = filter_tasks(tasks, False)
        results = search_tasks(pending_tasks, " GRAPH ")

        self.assertEqual(
            results,
            [{"id": 1, "title": "Practice graphs", "completed": False}] 
        )


    def test_undo_restores_pending_status(self):
        tasks = [
            {"id": 999, "title": "Practice graphs", "completed": True},
        ]

        undo_stack = [
            {"task_id": 999, "previous_completed": False},
        ]

        result = undo_status_change(tasks, undo_stack)

        self.assertTrue(result)
        self.assertFalse(tasks[0]["completed"])
        self.assertEqual(undo_stack, [])


    def test_undo_missing_task_preserves_stack(self):
        tasks = [
            {"id": 7, "title": "Practice graphs", "completed": True},
        ]

        undo_stack = [
            {"task_id": 999, "previous_completed": False},
        ]

        result = undo_status_change(tasks, undo_stack)

        self.assertFalse(result)

        # The existing task remains unchanged. 
        self.assertEqual(
            tasks, 
            [{"id": 7, "title": "Practice graphs", "completed": True}],
        )

        # The undo record remains available.
        self.assertEqual(
            undo_stack,
            [{"task_id": 999, "previous_completed": False}],
        )


    def test_undo_empty_stack_leaves_tasks_unchanged(self):
        tasks = [
            {"id": 7, "title": "Practice graphs", "completed": True},
        ]

        undo_stack = []

        result = undo_status_change(tasks, undo_stack)

        self.assertFalse(result)
        self.assertEqual(undo_stack, [])
        self.assertEqual(
            tasks, 
            [{"id": 7, "title": "Practice graphs", "completed": True}],
        )


    def test_undo_restores_latest_change_first(self):
        tasks = [
            {"id": 7, "title": "Practice graphs", "completed": True},
            {"id": 9, "title": "Review sorting", "completed": False},
        ]

        undo_stack = [
            {"task_id": 7, "previous_completed": False},
            {"task_id": 9, "previous_completed": True},
        ]

        result = undo_status_change(tasks, undo_stack)

        self.assertTrue(result)
        self.assertTrue(tasks[0]["completed"])
        self.assertTrue(tasks[1]["completed"])
        self.assertEqual(
            undo_stack,
            [{"task_id": 7, "previous_completed": False}],
        )


    def test_summary_counts_completed_and_pending_tasks(self):
        tasks = [
            {"id": 1, "title": "Graphs", "completed": True},
            {"id": 2, "title": "Sorting", "completed": False},
            {"id": 3, "title": "Trees", "completed": True},
        ]

        result = get_task_summary(tasks)

        self.assertEqual(
            result, 
            {"total": 3, "completed": 2, "pending": 1},
        )


    def test_summary_of_empty_tasks_returns_zero_counts(self):
        tasks = []

        result = get_task_summary(tasks)

        self.assertEqual(
            result,
            {"total": 0, "completed": 0, "pending": 0},

        )



    def test_load_tasks_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tasks.json"
            malformed_data = '[{"id": 1'
            file_path.write_text(malformed_data, encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                load_tasks(file_path)

            self.assertEqual(
                file_path.read_text(encoding="utf-8"),
                malformed_data,
            )


    def test_gui_stops_when_saved_json_is_invalid(self):
        error = json.JSONDecodeError("Invalid JSON", "", 0)

        with (
            patch("gui.tk.Tk") as mock_tk,
            patch("gui.load_tasks", side_effect=error),
            patch("gui.ttk.Frame"), 
            patch("gui.ttk.Label"),
            patch("gui.ttk.Entry"),
            patch("gui.ttk.Button"),
            patch("gui.messagebox.showerror") as mock_showerror,
            patch("gui.save_tasks") as mock_save,
        ):
            window = mock_tk.return_value

            gui.main()

            mock_showerror.assert_called_once()
            window.destroy.assert_called_once()
            window.mainloop.assert_not_called()
            mock_save.assert_not_called()



    def test_validate_tasks_rejects_duplicate_ids(self):
        tasks = [
            {"id": 1, "title": "Graphs", "completed": False},
            {"id": 1, "title": "Sorting", "completed": True},
        ]

        with self.assertRaisesRegex(ValueError, "Duplicate task ID"):
            validate_tasks(tasks)



    def test_validate_tasks_accepts_valid_data(self):
        tasks = [
            {"id": 1, "title": "Graphs", "completed": False},
            {"id": 2, "title": "Sorting", "completed": True},
        ]

        self.assertIsNone(validate_tasks(tasks))



    def test_load_tasks_rejects_duplicate_ids_without_changing_file(self):
        tasks = [
            {"id": 1, "title": "Graphs", "completed": False},
            {"id": 1, "title": "Sorting", "completed": True},
        ]

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tasks.json"
            saved_text = json.dumps(tasks)
            file_path.write_text(saved_text, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate task ID"):
                load_tasks(file_path)

            self.assertEqual(
                file_path.read_text(encoding="utf-8"),
                saved_text,
            )



    def test_gui_stops_when_saved_task_data_is_invalid(self):
        error = ValueError("Duplicate task ID: 1.")

        with (
            patch("gui.load_tasks", side_effect=error),
            patch("gui.tk.Tk") as mock_tk,
            patch("gui.ttk.Frame"), 
            patch("gui.ttk.Label"),
            patch("gui.ttk.Entry"),
            patch("gui.ttk.Button"),
            patch("gui.messagebox.showerror") as mock_showerror,
            patch("gui.save_tasks") as mock_save,
        ):
            window = mock_tk.return_value

            gui.main()

            mock_showerror.assert_called_once()
            window.destroy.assert_called_once()
            window.mainloop.assert_not_called()
            mock_save.assert_not_called()

            message = mock_showerror.call_args.args[1]
            self.assertIn("Duplicate task ID: 1.", message)



    def test_sort_tasks_by_title_ignores_case_and_preserves_input(self):
        tasks = [
            {"id": 1, "title": "Trees", "completed": False},
            {"id": 2, "title": "arrays", "completed": True},
            {"id": 3, "title": "Graphs", "completed": False},
        ]

        result = sort_tasks_by_title(tasks)

        sorted_ids = [task["id"] for task in result]
        original_ids = [task["id"] for task in tasks]

        self.assertEqual(sorted_ids, [2, 3, 1])
        self.assertEqual(original_ids, [1, 2, 3])



    def test_save_tasks_replaces_existing_file(self):
        tasks = [
            {"id": 1, "title": "Graphs", "completed": False},
        ]

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tasks.json"
            file_path.write_text("[]", encoding="utf-8")

            save_tasks(tasks, file_path)

            saved_data = json.loads(
                file_path.read_text(encoding="utf-8")
            )

            self.assertEqual(saved_data, tasks)
            self.assertEqual(
                set(Path(directory).iterdir()),
                {file_path},
            )



    def test_failed_save_preserves_existing_file(self):
        tasks = [
            {"id": 1, "title": "Graphs", "completed": False},
        ]

        def fail_during_write(data, file, **kwargs):
            file.write('[{"id":')
            raise OSError("Simulated write failure")

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "tasks.json"
            original_text = "[]"
            file_path.write_text(original_text, encoding="utf-8")

            with patch("planner.json.dump", side_effect=fail_during_write):
                with self.assertRaises(OSError):
                    save_tasks(tasks, file_path)

            self.assertEqual(
                file_path.read_text(encoding="utf-8"),
                original_text,
            )
            self.assertEqual(
                set(Path(directory).iterdir()),
                {file_path},
            )


# Run it from terminal below: python -m unittest -v

if __name__ == "__main__":
    unittest.main()



