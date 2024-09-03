from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Курс"""
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Урок"""
    class Meta:
        model = Lesson
        fields = '__all__'
