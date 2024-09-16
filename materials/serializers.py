from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_link_to_video


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Курс, добавлено динамическое поле"""

    count_lesson = SerializerMethodField()
    lessons = SerializerMethodField()
    is_subscription = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, course):
        """Метод возвращает количество уроков для объекта"""
        return course.lesson_set.count()

    def get_lessons(self, course):
        """Метод возвращает список уроков для объекта course"""
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_is_subscription(self, course):
        """Метод возвращает True, если у текущего пользователя есть подписка на данный курс"""
        return Subscription.objects.filter(user=self.context['request'].user, course=course).exists()


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Урок"""

    link_to_video = serializers.CharField(validators=[validate_link_to_video])

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Класс-сериализатор для модели Подписки"""

    class Meta:
        model = Subscription
        fields = "__all__"
