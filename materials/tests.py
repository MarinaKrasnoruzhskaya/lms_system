from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    """ Класс для тестирования работы CRUD уроков """

    def setUp(self):
        self.user = User.objects.create(email='test_user@lms.com')
        self.owner = User.objects.create(email='test_user_owner@lms.com')
        self.moderator = User.objects.create(email='test_moderator@lms.com')
        self.group = Group.objects.create(name='moderator')
        self.moderator.groups.add(self.group)

        self.course = Course.objects.create(title='тест курс', owner=self.owner)
        self.lesson = Lesson.objects.create(title='тест урок', course=self.course, owner=self.owner)
        self.new_lesson = Lesson.objects.create(title='тест урок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.owner)

    def test_lesson_retrieve(self):
        """ Тестирование просмотра урока владельцем"""

        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'),
            self.lesson.title
        )

    def test_lesson_retrieve_non_owner(self):
        """ Тестирование просмотра урока не владельцем"""

        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_retrieve_moderator(self):
        """ Тестирование просмотра урока модератором """

        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve_moderator_unauthorized(self):
        """ Тестирование просмотра урока неавторизованным пользователем """

        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_create(self):
        """ Тестирование создания урока авторизованным пользователем """

        url = reverse("materials:lesson-create")
        data = {
            "title": "тест урок 2",
            "link_to_video": "http://youtube.com/watch?v="
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            3
        )

    def test_lesson_create_moderator(self):
        """ Тестирование создания урока модератором """

        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lesson-create")
        data = {
            "title": "тест урок 2",
            "link_to_video": "http://youtube.com/watch?v="
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_create_unauthorized(self):
        """ Тестирование создания урока неавторизованным пользователем"""

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-create")
        data = {
            "title": "тест урок 2",
            "link_to_video": "http://youtube.com/watch?v="
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_create_not_valid_url(self):
        """ Тестирование попытки создания урока с невалидной ссылкой на видео"""

        url = reverse("materials:lesson-create")
        data = {
            "title": "тест урок 3",
            "link_to_video": "http://lesson.com/watch?v="
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_update(self):
        """ Тестирование редактирования урока владельцем"""

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title': 'Новый тест урок',
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('title'),
            'Новый тест урок'
        )

    def test_lesson_update_non_owner(self):
        """ Тестирование редактирования урока не владельцем"""

        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title': 'Новый тест урок',
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_update_moderator(self):
        """ Тестирование редактирования урока модератором"""

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title': 'Новый тест урок',
        }
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update_unauthorized(self):
        """ Тестирование редактирования урока неавторизованным пользователем """

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title': 'Новый тест урок',
        }
        self.client.force_authenticate(user=None)
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_delete(self):
        """ Тестирование удаления урока владельцем"""

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            1
        )

    def test_lesson_delete_non_owner(self):
        """ Тестирование удаления урока не владельцем"""

        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_delete_moderator(self):
        """ Тестирование удаления урока модератором """

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_delete_unauthorized(self):
        """ Тестирование удаления урока неавторизованным пользователем """

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        self.client.force_authenticate(user=None)
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_list(self):
        """ Тестирование просмотра списка уроков владельца"""

        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_to_video": None,
                    "title": self.lesson.title,
                    "description": None,
                    "picture": None,
                    "course": self.course.pk,
                    "owner": self.owner.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )

    def test_lesson_list_moderator(self):
        """ Тестирование просмотра списка всех уроков модератором"""

        url = reverse('materials:lesson-list')
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_to_video": None,
                    "title": self.lesson.title,
                    "description": None,
                    "picture": None,
                    "course": self.course.pk,
                    "owner": self.owner.pk
                },
                {
                    "id": self.new_lesson.pk,
                    "link_to_video": None,
                    "title": self.new_lesson.title,
                    "description": None,
                    "picture": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )

    def test_lesson_list_unauthorized(self):
        """ Тестирование просмотра списка  уроков неавторизованным пользователем"""

        url = reverse('materials:lesson-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class SubscriptionTestCase(APITestCase):
    """ Класс для тестирования подписки на обновление курса """

    def setUp(self):
        self.user = User.objects.create(email='test@lms.com')
        self.course_for_deactive = Course.objects.create(title='тест курс', owner=self.user)
        self.course_for_active = Course.objects.create(title='тест курс 2', owner=self.user)
        self.client.force_authenticate(user=self.user)
        self.subscription = Subscription.objects.create(course=self.course_for_deactive, user=self.user)

    def test_deactive_subscription(self):
        """ Тестирование деактивации подписки на обновление курса авторизованным пользователем"""

        url = reverse("materials:subscription")
        data = {
            "course": self.course_for_deactive.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['message'],
            'подписка удалена'
        )

    def test_deactive_subscription_unauthorized(self):
        """ Тестирование деактивации подписки на обновление курса неавторизованным пользователем"""

        self.client.force_authenticate(user=None)
        url = reverse("materials:subscription")
        data = {
            "course": self.course_for_deactive.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_active_subscription(self):
        """ Тестирование активации подписки на обновление курса авторизованным пользователем"""

        url = reverse("materials:subscription")
        data = {
            "course": self.course_for_active.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['message'],
            'подписка добавлена'
        )

    def test_active_subscription_unauthorized(self):
        """ Тестирование активации подписки на обновление курса неавторизованным пользователем"""

        self.client.force_authenticate(user=None)
        url = reverse("materials:subscription")
        data = {
            "course": self.course_for_active.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
