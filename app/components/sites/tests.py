from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Site


class SiteAPITests(APITestCase):

    def setUp(self):
        self.url_list = 'sites_api:site-list'
        self.url_detail = 'sites_api:site-detail'

        self.manager_user_password = 'manager_password'
        self.manager_user = User.objects.create(
            username='manager', password=self.manager_user_password)

        self.registered_user_password = 'test_password'
        self.registered_user = User.objects.create(
            username='user', password=self.registered_user_password)

        self.create_params = (reverse(self.url_list), {
            'url': 'https://github.com', 'is_private': True
        })

        Site.objects.bulk_create([
            Site(url='https://google.com'),
            Site(url='https://instagram.com', is_private=True),
        ])

    def test_anonymous_user_only_public_sites_list(self):
        response = self.client.get(reverse(self.url_list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'url': 'https://google.com', 'is_private': False}
        ])

    def test_anonymous_user_only_public_sites_detail(self):
        response = self.client.get(reverse(self.url_detail, args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'url': 'https://google.com', 'is_private': False
        })

    def test_anonymous_user_only_public_sites_detail_forbidden(self):
        response = self.client.get(reverse(self.url_detail, args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_private_sites_list(self):
        self.client.login(
            username=self.registered_user,
            password=self.registered_user_password)

        response = self.client.get(reverse(self.url_list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {'url': 'https://google.com', 'is_private': False},
            {'url': 'https://instagram.com', 'is_private': True}
        ])

    def test_authenticated_user_private_sites_detail(self):
        self.client.login(
            username=self.registered_user,
            password=self.registered_user_password)

        response = self.client.get(reverse(self.url_detail, args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'url': 'https://google.com', 'is_private': False
        })

        response = self.client.get(reverse(self.url_detail, args=(2,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'url': 'https://instagram.com', 'is_private': True
        })

    def test_creating_new_site_by_anonymous(self):
        response = self.client.post(*self.create_params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_new_site_by_other_registered_user(self):
        self.client.login(
            username=self.registered_user,
            password=self.registered_user_password)
        response = self.client.post(*self.create_params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creating_new_site_by_username_manager(self):
        self.client.login(
            username=self.manager_user,
            password=self.manager_user_password)
        response = self.client.post(*self.create_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_url_name(self):
        self.client.login(
            username=self.manager_user,
            password=self.manager_user_password)
        response = self.client.post(*self.create_params)
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
