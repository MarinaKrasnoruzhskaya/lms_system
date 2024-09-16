from django.contrib.auth.models import Group
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginator import CustomPagination
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet-класс для модели Курс"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """ Метод для ограничения доступа к эндпоинтам"""
        if self.action in ['create', 'destroy']:
            self.permission_classes = (IsAuthenticated, ~IsModerator,)
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = (IsAuthenticated, IsModerator | IsOwner,)
        elif self.action in ['list']:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """ Метод для автоматической привязки создаваемого объекта к авторизованному пользователю"""
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     """ Метод возвращает для 'list' только курсы владельца или все курсы для модератора"""
    #     queryset = super().get_queryset()
    #     if self.action == 'list':
    #         if IsModerator().has_permission(self.request, self):
    #             return queryset
    #         return queryset.filter(owner=self.request.user)
    #     return queryset


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
    pagination_class = CustomPagination

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


class SubscriptionAPIView(APIView):
    """Класс-контроллер для установки подписки пользователя и на удаление подписки у пользователя"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
