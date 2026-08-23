from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext

from statuses.models import Status
from tasks.models import Task

from .models import Label


class LabelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='label-user',
            password='test-password',
        )
        self.label = Label.objects.create(name='bug')

    def assert_message(self, response, message):
        self.assertContains(response, gettext(message))

    def test_anonymous_user_is_redirected_from_label_pages(self):
        urls = [
            reverse('labels_index'),
            reverse('labels_create'),
            reverse('labels_update', args=[self.label.pk]),
            reverse('labels_delete', args=[self.label.pk]),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, f'{reverse("login")}?next={url}')

    def test_list_displays_labels(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('labels_index'))

        self.assertContains(response, self.label.name)
        self.assertContains(response, gettext('Create label'))

    def test_create_label(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('labels_create'),
            {'name': 'feature'},
            follow=True,
        )

        self.assertTrue(Label.objects.filter(name='feature').exists())
        self.assert_message(response, 'Label successfully created')

    def test_label_name_must_be_unique(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('labels_create'),
            {'name': self.label.name},
        )

        self.assertContains(
            response,
            gettext('A label with this name already exists.'),
        )

    def test_update_label(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('labels_update', args=[self.label.pk]),
            {'name': 'documentation'},
            follow=True,
        )

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'documentation')
        self.assert_message(response, 'Label successfully updated')

    def test_delete_unused_label(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('labels_delete', args=[self.label.pk]),
            follow=True,
        )

        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())
        self.assert_message(response, 'Label successfully deleted')

    def test_cannot_delete_label_used_by_task(self):
        status = Status.objects.create(name='New')
        task = Task.objects.create(
            name='Task with label',
            status=status,
            author=self.user,
        )
        task.labels.add(self.label)
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('labels_delete', args=[self.label.pk]),
            follow=True,
        )

        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())
        self.assert_message(response, 'Unable to delete label')
