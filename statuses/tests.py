from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext

from .models import Status


class StatusTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='status-manager',
            password='password',
        )
        self.status = Status.objects.create(name='В работе')

    def assert_message(self, response, message):
        response_messages = [
            str(item) for item in get_messages(response.wsgi_request)
        ]
        self.assertIn(gettext(message), response_messages)

    def test_anonymous_user_is_redirected_to_login(self):
        statuses_url = reverse('statuses_index')

        response = self.client.get(statuses_url)

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={statuses_url}',
        )

    def test_statuses_list(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('statuses_index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_string_representation(self):
        self.assertEqual(str(self.status), self.status.name)

    def test_user_can_create_status(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('statuses_create'),
            {'name': 'Завершён'},
        )

        self.assertRedirects(
            response,
            reverse('statuses_index'),
            fetch_redirect_response=False,
        )
        self.assertTrue(Status.objects.filter(name='Завершён').exists())
        self.assert_message(response, 'Status successfully created')

    def test_user_cannot_create_status_with_duplicate_name(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('statuses_create'),
            {'name': self.status.name},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.context['form'].errors)
        self.assertContains(
            response,
            gettext('A status with this name already exists.'),
        )
        statuses_count = Status.objects.filter(
            name=self.status.name,
        ).count()
        self.assertEqual(statuses_count, 1)

    def test_user_can_update_status(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('statuses_update', args=[self.status.pk]),
            {'name': 'На проверке'},
        )

        self.assertRedirects(
            response,
            reverse('statuses_index'),
            fetch_redirect_response=False,
        )
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'На проверке')
        self.assert_message(response, 'Status successfully updated')

    def test_user_can_open_and_delete_status(self):
        self.client.force_login(self.user)
        delete_url = reverse('statuses_delete', args=[self.status.pk])

        response = self.client.get(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

        response = self.client.post(delete_url)

        self.assertRedirects(
            response,
            reverse('statuses_index'),
            fetch_redirect_response=False,
        )
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
        self.assert_message(response, 'Status successfully deleted')
