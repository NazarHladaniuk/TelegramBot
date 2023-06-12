from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

from telebot.models import Task


class ModelsTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="task1", description="description1",
        )

    def test_task_model_str(self):
        self.assertEqual(str(self.task), "task1")

    def test_task_model_completed(self):
        self.assertFalse(self.task.completed)

    def test_task_model_due_date(self):
        self.assertIsNotNone(self.task.due_date)


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(
            title="task1", description="description1",
        )
        self.task_data = {
            "title": "New Task",
            "description": "New Description",
            "due_date": "2023-07-25",
            "completed": False,
        }

    def test_get_all_tasks(self):
        url = reverse("telebot:task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_single_task(self):
        url = reverse("telebot:task-detail", args=[self.task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "task1")

    def test_create_task(self):
        url = reverse("telebot:task-list")
        response = self.client.post(url, self.task_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.last().title, "New Task")

    def test_update_task(self):
        url = reverse("telebot:task-detail", args=[self.task.id])
        response = self.client.put(url, self.task_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "New Task")

    def test_delete_task(self):
        url = reverse("telebot:task-detail", args=[self.task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
