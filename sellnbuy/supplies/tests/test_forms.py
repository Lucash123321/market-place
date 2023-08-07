from django.test import TestCase, Client
from supplies.models import User, Supply, Comment, Message
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class TestForms(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user('author')
        cls.first_user = User.objects.create_user('first_user')
        cls.supply = Supply.objects.create(user=cls.author, name='Тестовый товар', price=999)

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_supply_form(self):
        count = Supply.objects.count()
        data = {'name': 'Товар создан', 'price': 999, 'desc': 'Уникальное описание'}
        response = self.author_client.post(reverse('supplies:add_supply'), data, follow=True)
        self.assertEqual(Supply.objects.count(), count + 1)
        self.assertRedirects(response, reverse('supplies:profile', kwargs={'username': self.author.username}))
        self.assertTrue(Supply.objects.get(user=self.author, **data))

    def test_comment_form(self):
        count = Comment.objects.count()
        supply = Supply.objects.create(user=self.first_user, name='Тестовый товар', price=999)
        data = {'rating': '5', 'text': 'Уникальный комментарий'}
        response = self.author_client.post(reverse('supplies:add_comment', kwargs={'id': supply.id}), data, follow=True)
        self.assertEqual(Comment.objects.count(), count + 1)
        self.assertRedirects(response, reverse('supplies:supply', kwargs={'id': supply.id}))
        self.assertTrue(Comment.objects.get(user=self.author, **data))

    def test_message_form(self):
        count = Message.objects.count()
        data = {'text': 'Уникальное сообщение'}
        response_data = {'username': self.first_user}
        response = self.author_client.post(reverse('supplies:send_message', kwargs=response_data), data, follow=True)
        self.assertEqual(Message.objects.count(), count + 1)
        self.assertRedirects(response, reverse('supplies:chat', kwargs={'username': self.first_user}))
        self.assertTrue(Message.objects.get(user=self.author, **data))

    def test_change_supply_form(self):
        count = Supply.objects.count()
        response_data = {'id': self.supply.id}
        data = {'name': 'Измененный товар', 'price': 99, 'desc': 'Измененное описание'}
        response = self.author_client.post(reverse('supplies:change_supply', kwargs=response_data), data, follow=True)
        self.assertRedirects(response, reverse("supplies:supply", kwargs={'id': self.supply.id}))
        self.assertEqual(count, Supply.objects.count())
        self.assertTrue(Supply.objects.get(**data))
