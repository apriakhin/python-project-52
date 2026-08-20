from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext


class UserTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.get(pk=1)
        self.other_user = user_model.objects.get(pk=2)

    def assert_message(self, response, message):
        response_messages = [
            str(item) for item in get_messages(response.wsgi_request)
        ]
        self.assertIn(gettext(message), response_messages)

    def test_user_registration(self):
        response = self.client.post(
            reverse('users_create'),
            {
                'username': 'new-user',
                'first_name': 'New',
                'last_name': 'User',
                'password1': 'new-password',
                'password2': 'new-password',
            },
        )

        self.assertRedirects(
            response,
            reverse('login'),
            fetch_redirect_response=False,
        )
        created_user = get_user_model().objects.get(username='new-user')
        self.assertEqual(created_user.first_name, 'New')
        self.assertEqual(created_user.last_name, 'User')
        self.assertTrue(created_user.check_password('new-password'))
        self.assert_message(response, 'User successfully registered')

    def test_user_registration_with_invalid_data(self):
        response = self.client.post(
            reverse('users_create'),
            {
                'username': 'new-user',
                'first_name': 'New',
                'last_name': 'User',
                'password1': 'first-password',
                'password2': 'second-password',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(
            get_user_model().objects.filter(username='new-user').exists()
        )

    def test_user_can_update_themselves(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]),
            {
                'username': 'updated-john',
                'first_name': 'Updated',
                'last_name': 'Name',
                'password1': 'updated-password',
                'password2': 'updated-password',
            },
        )

        self.assertRedirects(
            response,
            reverse('users_index'),
            fetch_redirect_response=False,
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updated-john')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertTrue(self.user.check_password('updated-password'))
        self.assert_message(response, 'User successfully updated')

    def test_user_cannot_update_another_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', args=[self.other_user.pk]),
            {
                'username': 'changed-jane',
                'first_name': 'Changed',
                'last_name': 'User',
                'password1': 'changed-password',
                'password2': 'changed-password',
            },
        )

        self.assertRedirects(
            response,
            reverse('users_index'),
            fetch_redirect_response=False,
        )
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, 'jane')
        self.assert_message(
            response,
            'You do not have permission to edit this user',
        )

    def test_anonymous_user_cannot_update_user(self):
        update_url = reverse('users_update', args=[self.user.pk])

        response = self.client.get(update_url)

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={update_url}',
        )

    def test_user_can_delete_themselves(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', args=[self.user.pk]),
        )

        self.assertRedirects(
            response,
            reverse('users_index'),
            fetch_redirect_response=False,
        )
        self.assertFalse(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )
        self.assert_message(response, 'User successfully deleted')

    def test_user_cannot_delete_another_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', args=[self.other_user.pk]),
        )

        self.assertRedirects(
            response,
            reverse('users_index'),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.other_user.pk).exists()
        )
        self.assert_message(
            response,
            'You do not have permission to delete this user',
        )

    def test_anonymous_user_cannot_delete_user(self):
        delete_url = reverse('users_delete', args=[self.user.pk])

        response = self.client.get(delete_url)

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={delete_url}',
        )
