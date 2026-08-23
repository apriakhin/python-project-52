from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext

from labels.models import Label
from statuses.models import Status

from .models import Task


class TaskTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.author = user_model.objects.create_user(
            username='author',
            password='password',
        )
        self.executor = user_model.objects.create_user(
            username='executor',
            password='password',
        )
        self.other_user = user_model.objects.create_user(
            username='other-user',
            password='password',
        )
        self.status = Status.objects.create(name='В работе')
        self.label = Label.objects.create(name='Срочно')
        self.task = Task.objects.create(
            name='Подготовить релиз',
            description='Проверить изменения перед выпуском.',
            status=self.status,
            author=self.author,
            executor=self.executor,
        )
        self.task.labels.add(self.label)

    def assert_message(self, response, message):
        response_messages = [
            str(item) for item in get_messages(response.wsgi_request)
        ]
        self.assertIn(gettext(message), response_messages)

    def test_anonymous_user_is_redirected_from_all_task_pages(self):
        urls = [
            reverse('tasks_index'),
            reverse('tasks_create'),
            reverse('tasks_detail', args=[self.task.pk]),
            reverse('tasks_update', args=[self.task.pk]),
            reverse('tasks_delete', args=[self.task.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f'{reverse("login")}?next={url}',
                )

    def test_user_can_view_tasks_list_and_detail(self):
        self.client.force_login(self.author)

        list_response = self.client.get(reverse('tasks_index'))
        detail_response = self.client.get(
            reverse('tasks_detail', args=[self.task.pk]),
        )

        self.assertContains(list_response, self.task.name)
        self.assertContains(detail_response, self.task.description)
        self.assertContains(detail_response, self.label.name)

    def test_user_can_create_task(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('tasks_create'),
            {
                'name': 'Настроить мониторинг',
                'description': 'Добавить проверку ошибок.',
                'status': self.status.pk,
                'executor': self.executor.pk,
                'labels': [self.label.pk],
            },
        )

        self.assertRedirects(
            response,
            reverse('tasks_index'),
            fetch_redirect_response=False,
        )
        task = Task.objects.get(name='Настроить мониторинг')
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.executor, self.executor)
        self.assertTrue(task.labels.filter(pk=self.label.pk).exists())
        self.assert_message(response, 'Task successfully created')

    def test_user_cannot_create_task_with_duplicate_name(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('tasks_create'),
            {
                'name': self.task.name,
                'description': '',
                'status': self.status.pk,
                'executor': '',
                'labels': [],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
        self.assertContains(
            response,
            gettext('A task with this name already exists.'),
        )

    def test_user_can_update_task(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('tasks_update', args=[self.task.pk]),
            {
                'name': 'Подготовить выпуск',
                'description': 'Обновлённое описание.',
                'status': self.status.pk,
                'executor': '',
                'labels': [],
            },
        )

        self.assertRedirects(
            response,
            reverse('tasks_index'),
            fetch_redirect_response=False,
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Подготовить выпуск')
        self.assertIsNone(self.task.executor)
        self.assert_message(response, 'Task successfully updated')

    def test_only_author_can_delete_task(self):
        delete_url = reverse('tasks_delete', args=[self.task.pk])
        self.client.force_login(self.other_user)

        response = self.client.post(delete_url)

        self.assertRedirects(
            response,
            reverse('tasks_index'),
            fetch_redirect_response=False,
        )
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        self.assert_message(response, 'Only the task author can delete it')

        self.client.force_login(self.author)
        response = self.client.post(delete_url)

        self.assertRedirects(
            response,
            reverse('tasks_index'),
            fetch_redirect_response=False,
        )
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        self.assert_message(response, 'Task successfully deleted')

    def test_cannot_delete_status_used_by_task(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('statuses_delete', args=[self.status.pk]),
        )

        self.assertRedirects(
            response,
            reverse('statuses_index'),
            fetch_redirect_response=False,
        )
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        self.assert_message(response, 'Unable to delete status')

    def test_cannot_delete_user_related_to_task(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse('users_delete', args=[self.author.pk]),
        )

        self.assertRedirects(
            response,
            reverse('users_index'),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.author.pk).exists(),
        )
        self.assert_message(response, 'Unable to delete user')
