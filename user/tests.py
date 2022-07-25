from django.test import TestCase
from django.urls import resolve
from user.models import User
from django.urls import reverse
from rest_framework import status


class TestLoginRegistrationURL(TestCase):
    def test_login_user_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_registration_user_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'


class TestLoginRegistrationModel(TestCase):
    def test_should_create_user(self):
        user = User.objects.create_user(name='abhilash', email='abhilash@gmail.com')
        user.set_password("12345678")
        user.save()
        self.assertEqual(str(user), 'abhilash@gmail.com')


class TestLoginRegistrationView(TestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {'name': 'abhi', 'email': 'abhi@gmail.com', 'password': '12345678', 'password2': '12345678'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_with_correct_input_success(self):
        credentials = {
            'email': 'admin@gmail.com',
            'password': '12345678'}
        User.objects.create_user(**credentials)
        url = reverse('login')
        response = self.client.post(url, credentials, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)






