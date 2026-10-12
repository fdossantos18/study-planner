import unittest

from planner import rename_task, set_task_completed, filter_tasks, search_tasks, undo_status_change

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


# Run it from terminal below: python -m unittest -v

if __name__ == "__main__":
    unittest.main()



