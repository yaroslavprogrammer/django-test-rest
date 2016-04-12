from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Site


class SiteAPITests(APITestCase):

    def setUp(self):
        self.url = 'sites:api'

        self.manager_user_password = 'manager_password'
        self.manager_user = User.objects.create(
            username='manager', password=self.manager_user_password)

        self.registered_user_password = 'test_password'
        self.registered_user = User.objects.create(
            username='user', password=self.registered_user_password)

        Site.objects.bulk_create([
            Site(url='https://google.com'),
            Site(url='https://instagram.com', is_private=True),
        ])

    def test_anonymous_user_only_public_sites_list_and_by_key(self):
        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'url': 'https://google.com', 'is_private': False}
        ])

        response = self.client.get(reverse(self.url, args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'url': 'https://google.com', 'is_private': False
        })

        response = self.client.get(reverse(self.url, args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_private_sites_list_and_by_key(self):
        self.client.login(
            username=self.registered_user,
            password=self.registered_user_password)

        response = self.client.get(reverse(self.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'url': 'https://google.com', 'is_private': False},
            {'url': 'https://instagram.com', 'is_private': True}
        ])

        response = self.client.get(reverse(self.url, args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'url': 'https://google.com', 'is_private': False
        })

        response = self.client.get(reverse(self.url, args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'url': 'https://instagram.com', 'is_private': True
        })

        self.client.logout()

    def test_creating_new_site_by_anonymous_other_registered_and_manager(self):
        params = (reverse(self.url), {
            'url': 'https://github.com', 'is_private': True
        })

        response = self.client.post(*params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(
            username=self.registered_user,
            password=self.registered_user_password)
        response = self.client.post(*params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

        self.client.login(
            username=self.manager_user,
            password=self.manager_user_password)
        response = self.client.post(*params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_invalid_url_name(self):
        params = (reverse(self.url), {
            'url': 'http://github.com', 'is_private': True
        })

        self.client.login(
            username=self.manager_user,
            password=self.manager_user_password)
        response = self.client.post(*params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SiteModelTests(TestCase):

    def test_raise_not_https_model_on_save(self):
        with self.assertRaises(ValidationError):
            Site(url='http://test.com', is_private=True).save()

        s = Site(url='https://test.com', is_private=True)
        s.save()

        self.assertNotEqual(s.id, None)

    def test_raise_site_not_available(self):
        # TODO: needs mock when tester don't have internet connection
        # SLOW: will work faster if we use mocked of request

        with self.assertRaises(ValidationError):
            Site(url='https://asdsadsddas.com').save()

        Site(url='https://google.com').save()
