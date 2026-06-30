import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_dashboard_renders_without_firebase_configuration(self):
        user = get_user_model().objects.create_user(username='program_controller', password='Password123!')
        group, _ = Group.objects.get_or_create(name='program_controller')
        user.groups.add(group)
        self.client.force_login(user)

        with patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': '', 'FIREBASE_PROJECT_ID': ''}, clear=False):
            response = self.client.get('/', HTTP_HOST='127.0.0.1')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')


class AuthRoutingTests(TestCase):
    def _create_user(self, username, group_name):
        user = get_user_model().objects.create_user(username=username, password='Password123!')
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        return user

    def test_role_based_login_redirects_to_the_correct_dashboard(self):
        cases = [
            ('dean', 'dean_dashboard'),
            ('program_controller', 'dashboard'),
            ('instructor', 'instructor_dashboard'),
        ]

        for username, expected_url_name in cases:
            with self.subTest(username=username):
                self._create_user(username, username)
                response = self.client.post(
                    reverse('custom_login'),
                    {'username': username, 'password': 'Password123!'},
                    follow=True,
                )
                self.assertRedirects(response, reverse(expected_url_name))
                self.client.logout()
