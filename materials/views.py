from django.contrib.auth.models import Group
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для модели Курс"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """ Метод для ограничения доступа к эндпоинтам"""
        if self.action in ['create', 'destroy']:
            self.permission_classes = (IsAuthenticated, ~IsModerator,)
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """ Метод для автоматической привязки создаваемого объекта к авторизованному пользователю"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """ Метод возвращает для 'list' только курсы владельца или все курсы для модератора"""
        queryset = super().get_queryset()
        if self.action == 'list':
            if IsModerator().has_permission(self.request, self):
                return queryset
            return queryset.filter(owner=self.request.user)
        return queryset


class LessonCreateAPIView(CreateAPIView):
    """Класс-контроллер на основе базового класса дженерика для создания урока"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """ Метод для автоматической привязки создаваемого объекта к авторизованному пользователю"""
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def get_queryset(self):
        """ Метод возвращает только уроки владельца или все уроки для модератора"""
        queryset = super().get_queryset()
        if IsModerator().has_permission(self.request, self):
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения одного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    """Класс-контроллер на основе базового класса дженерика для редактирования урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    """Класс-контроллер на основе базового класса дженерика для удаления урока"""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
