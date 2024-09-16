from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_link_to_video


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Курс, добавлено динамическое поле"""

    count_lesson = SerializerMethodField()
    lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, course):
        """Метод возвращает количество уроков для объекта"""
        return course.lesson_set.count()

    def get_lessons(self, course):
        """Метод возвращает список уроков для объекта course"""
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Урок"""

    link_to_video = serializers.CharField(validators=[validate_link_to_video])

    class Meta:
        model = Lesson
        fields = "__all__"
