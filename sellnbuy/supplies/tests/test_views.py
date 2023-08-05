from django.test import TestCase, Client
from supplies.models import User, Supply, Comment, Message
from django.urls import reverse
from supplies.utils import Chat
from django.core.files.uploadedfile import SimpleUploadedFile


class TestView(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.first_user = User.objects.create_user('first_user')
        cls.second_user = User.objects.create_user('second_user')
        cls.author = User.objects.create_user('author')

        cls.image = (b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                     b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                     b'\x02\x4c\x01\x00\x3b')

        cls.uploaded = SimpleUploadedFile('image.png', cls.image)

        for number in range(1, 51):
            data = {"user": cls.author,
                    "name": f"Тестовый товар {number}",
                    "price": 999,
                    "desc": "Тестовое описание",
                    "image": cls.uploaded}
            Supply.objects.create(**data)

        supply = Supply.objects.get(id=1)
        for number in range(1, 51):
            data = {"user": cls.author, "supply": supply, "rating": "5", "text": f"Тестовый комментарий {number}"}
            Comment.objects.create(**data)

        for number in range(10):
            if number % 3:
                Message.objects.create(user=cls.first_user, to=cls.author, text=f'Сообщение №{number}')
            else:
                Message.objects.create(user=cls.author, to=cls.first_user, text=f'Сообщение №{number}')

        for number in range(10):
            if number < 5:
                Message.objects.create(user=cls.author, to=cls.second_user, text=f'Сообщение №{number}')
            else:
                Message.objects.create(user=cls.second_user, to=cls.author, text=f'Сообщение №{number}')

            cls.used_templates = {
                reverse("supplies:index"): "supplies/index.html",
                reverse("supplies:add_supply"): "supplies/add_supply.html",
                reverse("supplies:messanger"): "supplies/messanger.html",
                reverse("supplies:supply", kwargs={'id': 1}): "supplies/supply_page.html",
                reverse("supplies:profile", kwargs={'username': cls.first_user.username}): "supplies/profile.html",
                reverse("supplies:chat", kwargs={'username': cls.first_user.username}): "supplies/chat.html",
                reverse("supplies:change_supply", kwargs={'id': 1}): "supplies/add_supply.html",
                reverse("supplies:change_comment", kwargs={'id': 1}): "supplies/change_comment.html",
            }

    def setUp(self):
        self.first_user_client = Client()
        self.first_user_client.force_login(self.first_user)
        self.second_user_client = Client()
        self.second_user_client.force_login(self.second_user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_views_templates(self):
        for url, template in self.used_templates.items():
            response = self.author_client.get(url, follow=True)
            self.assertTemplateUsed(response, template)

    def test_index_context(self):
        data = list(Supply.objects.all())
        response = self.client.get(reverse("supplies:index"))
        self.assertEqual(data[:20], response.context.get('page_obj').object_list)
        response = self.client.get(reverse("supplies:index") + "?page=2")
        self.assertEqual(data[20:40], response.context.get('page_obj').object_list)
        response = self.client.get(reverse("supplies:index") + "?page=3")
        self.assertEqual(data[40:51], response.context.get('page_obj').object_list)

    def test_supply_page_context(self):
        data = list(Comment.objects.all().order_by('-id'))
        response = self.client.get(reverse("supplies:supply", kwargs={'id': 1}))
        self.assertEqual(data[:20], response.context.get('page_obj').object_list)
        response = self.client.get(reverse("supplies:supply", kwargs={"id": 1}) + "?page=2")
        self.assertEqual(data[20:40], response.context.get('page_obj').object_list)
        response = self.client.get(reverse("supplies:supply", kwargs={"id": 1}) + "?page=3")
        self.assertEqual(data[40:51], response.context.get('page_obj').object_list)

    def test_profile_context(self):
        data = list(Supply.objects.all())
        response = self.client.get(reverse("supplies:profile", kwargs={'username': 'author'}))
        self.assertEqual(data[:20], response.context.get('page_obj').object_list)
        response = self.client.get(reverse("supplies:profile", kwargs={'username': 'author'}) + "?page=2")
        self.assertEqual(data[20:40], response.context.get('page_obj').object_list)
        response = self.client.get(reverse("supplies:profile", kwargs={'username': 'author'}) + "?page=3")
        self.assertEqual(data[40:51], response.context.get('page_obj').object_list)

    def test_chat_context(self):
        response = self.first_user_client.get(reverse("supplies:chat", kwargs={'username': self.author.username}))
        self.assertEqual(response.context.get('messages'), Chat(self.first_user, self.author).list_of_messages())
        response = self.author_client.get(reverse("supplies:chat", kwargs={'username': self.second_user.username}))
        self.assertEqual(response.context.get('messages'), Chat(self.second_user, self.author).list_of_messages())

    def test_messanger(self):
        response = self.author_client.get(reverse("supplies:messanger"))
        self.assertEqual(len(response.context.get('chats')), 2)
        response = self.second_user_client.get(reverse("supplies:messanger"))
        self.assertEqual(len(response.context.get('chats')), 1)
        response = self.first_user_client.get(reverse("supplies:messanger"))
        self.assertEqual(len(response.context.get('chats')), 1)

    def test_supply_context(self):
        supply = Supply.objects.get(id=1)
        response = self.first_user_client.get(reverse("supplies:supply", kwargs={"id": 1}))
        self.assertEqual(response.context.get('supply'), supply)

