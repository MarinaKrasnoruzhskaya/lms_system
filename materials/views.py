from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ ViewSet-класс для модели Курс """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateAPIView(CreateAPIView):
    """ Класс-контроллер на основе базового класса дженерика для создания урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(ListAPIView):
    """ Класс-контроллер на основе базового класса дженерика для отображения списка уроков """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Класс-контроллер на основе базового класса дженерика для отображения одного урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(UpdateAPIView):
    """ Класс-контроллер на основе базового класса дженерика для редактирования урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(DestroyAPIView):
    """ Класс-контроллер на основе базового класса дженерика для удаления урока """
    queryset = Lesson.objects.all()
