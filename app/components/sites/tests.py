from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Site


class SiteAPITests(APITestCase):
    # TODO: needs mock when tester don't have internet connection
    # SLOW: will work faster if we use mocked of request

    @classmethod
    def setUpClass(cls):
        super(SiteAPITests, cls).setUpClass()

        cls.url_list = 'sites_api:site-list'
        cls.url_detail = 'sites_api:site-detail'

        cls.manager_user = User.objects.create_user('manager', password='test')
        cls.registered_user = User.objects.create_user('user', password='test')

        cls.create_params = (reverse(cls.url_list), {
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
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_private_sites_list(self):
        self.client.force_login(self.registered_user)

        response = self.client.get(reverse(self.url_list))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for item in response.data:
            self.assertIn(item, [
                {'url': 'https://google.com', 'is_private': False},
                {'url': 'https://instagram.com', 'is_private': True}
            ])

    def test_authenticated_user_private_sites_detail(self):
        self.client.force_login(self.registered_user)

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
        self.client.force_login(self.registered_user)
        response = self.client.post(*self.create_params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_creating_new_site_by_username_manager(self):
        self.client.force_login(self.manager_user)
        response = self.client.post(*self.create_params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_url_name(self):
        self.client.force_login(self.manager_user)
        response = self.client.post(reverse(self.url_list), {
            'url': 'http://github.com', 'is_private': True
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SiteModelTests(TestCase):

    def test_raise_not_https_url(self):
        with self.assertRaises(ValidationError):
            Site(url='http://test.com', is_private=True).save()

        s = Site(url='https://test.com', is_private=True)
        s.save()

        self.assertNotEqual(s.id, None)

    def test_raise_site_not_available(self):
        with self.assertRaises(ValidationError):
            Site(url='https://asdsadsddas.com').save()

        Site(url='https://google.com').save()
