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
from materials.permissions import IsModerator
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
            self.permission_classes = (IsModerator,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """Класс-контроллер на основе базового класса дженерика для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(ListAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonRetrieveAPIView(RetrieveAPIView):
    """Класс-контроллер на основе базового класса дженерика для отображения одного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    """Класс-контроллер на основе базового класса дженерика для редактирования урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    """Класс-контроллер на основе базового класса дженерика для удаления урока"""

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]
