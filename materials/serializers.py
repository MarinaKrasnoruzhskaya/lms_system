from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Курс, добавлено динамическое поле"""
    count_lesson = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, course):
        """ Метод возвращает количество уроков для объекта"""
        return course.lesson_set.count()


class LessonSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Урок"""
    class Meta:
        model = Lesson
        fields = '__all__'
