from django.contrib import admin

from materials.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "picture", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "picture", "link_to_video", "course", 'updated_at')


@admin.register(Subscription)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("user", "course")