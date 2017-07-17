# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models.functions import datetime
from django.test.client import Client
from django.urls.base import reverse
from django.utils import timezone
from django_webtest import WebTest
from authsystem.models import MyUser
from django.test.testcases import TransactionTestCase

# Create your tests here.
from messaging.models import Group, Message


class MyTest(WebTest):
    def setUp(self):
        self.user_hamid = MyUser.objects.create_user(username='hamid', password='mypassword',
                                                     first_name='john', last_name='wayne')
        self.user_ali = MyUser.objects.create_user(username='ali', password='mypassword',
                                                   first_name='john', last_name='wayne')
        self.group_hamid = Group.objects.create(name='hamid-group', creator=self.user_hamid)
        self.group_ali = Group.objects.create(name='ali-group', creator=self.user_ali)
        self.group_hamid.members.add(self.user_hamid)
        self.group_ali.members.add(self.user_ali)
        self.hamid_message = Message.objects.create(text="Hallo", author=self.user_hamid,
                                                    group=self.group_hamid)
        self.hamid_message2 = Message.objects.create(text="Hallolllllllllllllllllllllllllllllllll"
                                                          "llllllllllllllllllllllllllllllllllllll"
                                                          "llllllllllllllllllsssssssssssssssssss",
                                                     author=self.user_ali,
                                                     group=self.group_ali)

    def login(self, usr):
        form = self.app.get(reverse('authsystem:login')).form
        form['username'] = usr
        form['password'] = 'mypassword'
        response = form.submit().follow()
        return response

    def test_create_group(self):
        response = self.login('hamid')
        form = self.app.get(reverse('messaging:create-group')).forms[1]
        form['name'] = 'some_group'
        response = form.submit().follow()
        self.assertTrue(Group.objects.filter(name='some_group').exists())
        self.assertEqual(Group.objects.get(name='some_group').__str__(), 'some_group')

    def test_join(self):
        response = self.login('ali')
        form = self.app.get(reverse('messaging:group',
                                    kwargs={'group_id': self.group_hamid.id})).forms[0]
        form['group_id'] = self.group_hamid.id
        response = form.submit()
        self.assertTrue(self.user_ali in self.group_hamid.members.all())
        response = self.app.get(reverse('messaging:profile'))
        self.assertTrue(response.__contains__('hamid-group'))

    def test_send_message(self):
        response = self.login('hamid')
        form = self.app.get(reverse('messaging:group',
                                    kwargs={'group_id': self.group_hamid.id})).forms[1]
        form['group_id'] = self.group_hamid.id
        form['text'] = 'hello'
        response =form.submit().follow()
        self.assertContains(response, 'hello')

class MessagingTest(TransactionTestCase):
    def login(self, usr):
        return self.client.post(reverse('authsystem:login'), {'username': usr,
                                                              'password': 'mypassword'})

    def setUp(self):
        self.user_hamid = MyUser.objects.create_user(username='hamid', password='mypassword',
                                                     first_name='john', last_name='wayne')
        self.user_ali = MyUser.objects.create_user(username='ali', password='mypassword',
                                                   first_name='john', last_name='wayne')
        self.client = Client()
        self.group_hamid = Group.objects.create(name='hamid-group', creator=self.user_hamid)
        self.group_hamid.members.add(self.user_hamid)
#
#     def test_create_group(self):
#         response = self.login('hamid')
#         self.assertEqual(response.status_code, 302)
#         response = self.client.post(reverse('messaging:create-group'), {'name': 'some_group'})
#         self.assertTrue(Group.objects.filter(name='some_group').exists())
#         self.assertEqual(response.status_code, 302)
#         response = self.client.get(reverse('messaging:profile'))
#         self.assertContains(response, 'some_group')
#
#     def test_join(self):
#         response = self.login('ali')
#         self.assertEqual(response.status_code, 302)
#         response = self.client.post(reverse('messaging:join-group'),
#                                     {'group_id': self.group_hamid.id})
#         self.assertTrue(self.user_ali in self.group_hamid.members.all())
#
#     def test_send_message(self):
#         response = self.login('hamid')
#         self.assertEqual(response.status_code, 302)
#         response = self.client.post(reverse('messaging:group',
#                                             kwargs={'group_id': self.group_hamid.id}),
#                                     {'text': 'halllllo', 'group_id': self.group_hamid.id},
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'halllllo')

    def test_send_message_unauthorized(self):
        response = self.login("ali")

        response = self.client.post(reverse('messaging:group',
                                            kwargs={'group_id': self.group_hamid.id}),
                                    {'text': 'halllllo', 'group_id': self.group_hamid.id},
                                    follow=True)
        self.assertEqual(response.status_code, 403)
