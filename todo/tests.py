from todo.models import Task
from django.utils import timezone
from datetime import datetime
from django.test import TestCase, Client


# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample1(self) -> None:
        self.assertEqual(1 + 2, 3)


class TaskModelTestCase(TestCase):
    def test_create_task1(self) -> None:
        due: timezone.datetime | None = timezone.make_aware(
            datetime(2024, 6, 30, 23, 59, 59)
        )
        task: Task = Task(title="task1", due_at=due)
        task.save()
        task: Task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, "task1")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)

    def test_create_task2(self) -> None:
        task: Task = Task(title="task2")
        task.save()
        task: Task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, "task2")
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, None)

    def test_is_overdue_future(self) -> None:
        due: timezone.datetime | None = timezone.make_aware(
            datetime(2024, 6, 30, 23, 59, 59)
        )
        current: timezone.datetime | None = timezone.make_aware(
            datetime(2024, 6, 30, 0, 0, 0)
        )
        task: Task = Task(title="fail_task", due_at=due)
        task.save()
        self.assertFalse(task.is_overdue(current))

    def test_is_overdue_past(self) -> None:
        due: timezone.datetime | None = timezone.make_aware(
            datetime(2024, 6, 30, 23, 59, 59)
        )
        current: timezone.datetime | None = timezone.make_aware(
            datetime(2024, 7, 1, 0, 0, 0)
        )
        task: Task = Task(title="safe_task", due_at=due)
        task.save()
        self.assertTrue(task.is_overdue(current))

    def test_is_overdue_none(self) -> None:
        due: timezone.datetime | None = None
        current: timezone.datetime | None = timezone.make_aware(
            datetime(2024, 7, 1, 0, 0, 0)
        )
        task: Task = Task(title="none_task", due_at=due)
        task.save()
        self.assertFalse(task.is_overdue(current))


class TodoViewTestCase(TestCase):
    def test_index_get(self) -> None:
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/index.html")
        self.assertEqual(len(response.context["tasks"]), 0)

    def test_index_post(self) -> None:
        client = Client()
        data = {"title": "Test Task", "due_at": "2024-06-30 23:59:59"}
        response = client.post("/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "todo/index.html")
        self.assertEqual(len(response.context["tasks"]), 1)
