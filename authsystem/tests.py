# - normal sign up
# - sign up with repetitive username
# - sign up with wrong password
# - normal login
# - login with wrong combo


# Create your tests here.
from django.test.client import Client
from django.test.testcases import TransactionTestCase
from django.urls.base import reverse
from .models import MyUser


class SignUpTest(TransactionTestCase):
    def setUp(self):
        self.user_hamid = MyUser.objects.create_user(username='hamid', password='mypassword',
                                                     first_name='john', last_name='wayne')
        self.client = Client()

    def create_sign_up_data(self, username='john', password='mypassword',
                            re_password='mypassword'):
        return {'username': username, 'password1': password, 'password2': re_password,
                'first_name': 'john', 'last_name': 'smith'}

    def test_normal_sign_up(self):
        response = self.client.post(reverse('authsystem:signup'),
                                    self.create_sign_up_data())
        self.assertTrue(MyUser.objects.filter(username='john').exists())
        self.assertEqual(response.status_code, 302)

    def test_repetitive_sign_up(self):
        num_of_users = MyUser.objects.count()
        response = self.client.post(reverse('authsystem:signup'),
                                    self.create_sign_up_data(username='hamid'))
        self.assertTrue(
            b"A user with that username already exists." in response.content)
        self.assertEqual(MyUser.objects.count(), num_of_users)

    def test_wrong_password_sign_up(self):
        response = self.client.post(reverse('authsystem:signup'),
                                    self.create_sign_up_data(username='john',
                                                             re_password='fsadfsdfsdfsd'))
        self.assertTrue(
            b"The two password fields didn&#39;t match." in response.content)

    def test_normal_login(self):
        response = self.client.post(reverse('authsystem:login'),
                                    self.create_login_data())
        self.assertEqual(response.status_code, 302)

    def create_login_data(self, username='hamid', password='mypassword'):
        return {'username': username, 'password': password}

    def test_wrong_combo_login(self):
        response = self.client.post(reverse('authsystem:login'),
                                    self.create_login_data(username='hamid',
                                                           password='asfsdfsfds'))
        self.assertTrue(b"Please enter a correct username and password. "
                        b"Note that both fields may be case-sensitive."
                        in response.content)
