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
        cls.comment = Comment.objects.create(user=cls.first_user,
                                             supply=cls.supply,
                                             rating='5',
                                             text='Тестовый комментарий')
        cls.image = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                     b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                     b'\x02\x4c\x01\x00\x3b')

        cls.uploaded = SimpleUploadedFile('image.png', cls.image)

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.first_user_client = Client()
        self.first_user_client.force_login(self.first_user)

    def test_supply_form(self):
        count = Supply.objects.count()
        data = {'name': 'Товар создан', 'price': 999, 'desc': 'Уникальное описание', 'image': self.uploaded}
        response = self.author_client.post(reverse('supplies:add_supply'), data, follow=True)
        self.assertEqual(Supply.objects.count(), count + 1)
        self.assertRedirects(response, reverse('supplies:profile', kwargs={'username': self.author.username}))
        supply = Supply.objects.get(user=self.author, name=data['name'], price=data['price'], desc=data['desc'])
        self.assertTrue(supply)
        response = self.first_user_client.get(reverse("supplies:supply", kwargs={"id": supply.id}))
        self.assertEqual(response.context.get('supply'), supply)
        self.assertTrue(response.context.get('supply').image)

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
        self.assertTrue(Supply.objects.get(user=self.author, **data))

    def test_change_comment_form(self):
        count = Comment.objects.count()
        response_data = {'id': self.comment.id}
        data = {'rating': '5', 'text': 'Измененный комментарий'}
        response = self.first_user_client.post(reverse('supplies:change_comment', kwargs=response_data),
                                               data,
                                               follow=True)
        self.assertRedirects(response, reverse("supplies:supply", kwargs={'id': self.comment.supply.id}))
        self.assertEqual(count, Comment.objects.count())
        self.assertTrue(Comment.objects.get(user=self.first_user, **data))
