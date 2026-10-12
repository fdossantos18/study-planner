import unittest

from planner import rename_task, set_task_completed, filter_tasks, search_tasks

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

# Run it from terminal below: python -m unittest -v

if __name__ == "__main__":
    unittest.main()



