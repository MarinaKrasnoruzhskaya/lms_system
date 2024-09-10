from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
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


class LessonSerializer(ModelSerializer):
    """Класс-сериализатор для модели Урок"""

    class Meta:
        model = Lesson
        fields = "__all__"
