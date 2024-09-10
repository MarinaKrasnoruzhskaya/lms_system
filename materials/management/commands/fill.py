import json
import os

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import connection

from config.settings import BASE_DIR
from materials.models import Course, Lesson
from users.models import User, Payments


class Command(BaseCommand):
    """Класс для кастомной команды заполнения БД"""

    @staticmethod
    def json_read(name_file: str) -> dict:
        """Метод считывает данные из json-файла"""
        all_name_file = os.path.join(BASE_DIR, "materials", "fixtures", name_file)
        with open(all_name_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_read_data(name_file, name_app, name_model):
        """Метод читает данные из json-файла по конкретному приложению и модели"""
        data = []

        for item in Command.json_read(name_file):
            if item["model"] == f"{name_app}.{name_model}":
                data.append(item)

        return data

    @staticmethod
    def truncate_table_restart_id(name_app, name_model):
        """Метод очищает таблицу и обнуляет id=1"""
        with connection.cursor() as cursor:
            cursor.execute(
                f"TRUNCATE TABLE {name_app}_{name_model} RESTART IDENTITY CASCADE"
            )

    @staticmethod
    def select_setval_id(name_app, name_model):
        """Метод устанавливает последний id в таблице"""
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT SETVAL('{name_app}_{name_model}_id_seq', (SELECT MAX(id) FROM {name_app}_{name_model}));"
            )

    def handle(self, *args, **options):
        """Метод для заполнения БД"""
        # таблица contenttypes.contenttype

        ContentType.objects.all().delete()
        Command.truncate_table_restart_id("django", "content_type")

        contenttype_for_create = []

        for content in Command.json_read_data(
            "contenttypes_data.json", "contenttypes", "contenttype"
        ):
            contenttype_for_create.append(
                ContentType(
                    id=content["pk"],
                    app_label=content["fields"]["app_label"],
                    model=content["fields"]["model"],
                )
            )

        ContentType.objects.bulk_create(contenttype_for_create)
        Command.select_setval_id("django", "content_type")

        # таблица auth.permission

        Permission.objects.all().delete()
        Command.truncate_table_restart_id("auth", "permission")
        permission_for_create = []

        for perm in Command.json_read_data("auth_data.json", "auth", "permission"):
            permission_for_create.append(
                Permission(
                    id=perm["pk"],
                    name=perm["fields"]["name"],
                    content_type=ContentType.objects.get(
                        pk=perm["fields"]["content_type"]
                    ),
                    codename=perm["fields"]["codename"],
                )
            )

        Permission.objects.bulk_create(permission_for_create)
        Command.select_setval_id("auth", "permission")

        # таблица auth.group

        Group.objects.all().delete()
        Command.truncate_table_restart_id("auth", "group")
        group_for_create = []
        group_permissions = {}

        for group in Command.json_read_data("auth_data.json", "auth", "group"):
            permissions = []
            for perm_id in group["fields"]["permissions"]:
                permissions.append(Permission.objects.get(id=perm_id))
            group_permissions[group["pk"]] = permissions

            group_for_create.append(
                Group(
                    id=group["pk"],
                    name=group["fields"]["name"],
                )
            )

        Group.objects.bulk_create(group_for_create)
        Command.select_setval_id("auth", "group")

        for pk, permissions in group_permissions.items():
            group = Group.objects.get(pk=pk)
            group.permissions.set(permissions)

        # таблица users.user
        User.objects.all().delete()
        Command.truncate_table_restart_id("users", "user")

        user_for_create = []
        user_groups = {}
        user_permissions = {}
        for user in Command.json_read_data("users_data.json", "users", "user"):
            permissions = (
                [
                    Permission.objects.get(id=perm_id)
                    for perm_id in user["fields"]["user_permissions"]
                ]
                if user["fields"]["user_permissions"]
                else []
            )
            user_permissions[user["pk"]] = permissions
            groups = [
                Group.objects.get(pk=group_id) for group_id in user["fields"]["groups"]
            ]
            user_groups[user["pk"]] = groups
            user_for_create.append(
                User(
                    id=user["pk"],
                    password=user["fields"]["password"],
                    last_login=user["fields"]["last_login"],
                    is_superuser=user["fields"]["is_superuser"],
                    is_staff=user["fields"]["is_staff"],
                    is_active=user["fields"]["is_active"],
                    date_joined=user["fields"]["date_joined"],
                    email=user["fields"]["email"],
                    phone_number=user["fields"]["phone_number"],
                    city=user["fields"]["city"],
                    avatar=user["fields"]["avatar"],
                    first_name=user["fields"]["first_name"],
                    last_name=user["fields"]["last_name"],
                )
            )

        User.objects.bulk_create(user_for_create)
        Command.select_setval_id("users", "user")

        for pk, permissions in user_permissions.items():
            user = User.objects.get(pk=pk)
            user.user_permissions.set(permissions)

        for pk, groups in user_groups.items():
            user = User.objects.get(pk=pk)
            user.groups.set(groups)

        Course.objects.all().delete()
        Command.truncate_table_restart_id("materials", "course")

        course_for_create = []
        for course in Command.json_read_data(
            "materials_data.json", "materials", "course"
        ):
            course_for_create.append(
                Course(
                    id=course["pk"],
                    title=course["fields"]["title"],
                    picture=course["fields"]["picture"],
                    description=course["fields"]["description"],
                )
            )

        Course.objects.bulk_create(course_for_create)
        Command.select_setval_id("materials", "course")

        Lesson.objects.all().delete()
        Command.truncate_table_restart_id("materials", "lesson")

        lesson_for_create = []
        for lesson in Command.json_read_data(
            "materials_data.json", "materials", "lesson"
        ):
            lesson_for_create.append(
                Lesson(
                    id=lesson["pk"],
                    title=lesson["fields"]["title"],
                    description=lesson["fields"]["description"],
                    picture=lesson["fields"]["picture"],
                    link_to_video=lesson["fields"]["link_to_video"],
                    course=Course.objects.get(pk=lesson["fields"]["course"]),
                )
            )

        Lesson.objects.bulk_create(lesson_for_create)
        Command.select_setval_id("materials", "lesson")

        Payments.objects.all().delete()
        Command.truncate_table_restart_id("users", "payments")

        payments_for_create = []
        for payments in Command.json_read_data("users_data.json", "users", "payments"):
            paid_course = (
                Course.objects.get(pk=payments["fields"]["paid_course"])
                if payments["fields"]["paid_course"]
                else payments["fields"]["paid_course"]
            )
            paid_lesson = (
                Lesson.objects.get(pk=payments["fields"]["paid_lesson"])
                if payments["fields"]["paid_lesson"]
                else payments["fields"]["paid_lesson"]
            )
            payments_for_create.append(
                Payments(
                    id=payments["pk"],
                    user=User.objects.get(pk=payments["fields"]["user"]),
                    payment_date=payments["fields"]["payment_date"],
                    paid_course=paid_course,
                    paid_lesson=paid_lesson,
                    payment_amount=payments["fields"]["payment_amount"],
                    payment_method=payments["fields"]["payment_method"],
                )
            )

        Payments.objects.bulk_create(payments_for_create)
        Command.select_setval_id("users", "payments")
