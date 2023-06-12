from rest_framework import viewsets

from telebot.models import Task
from telebot.pagination import CustomPagination
from telebot.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
