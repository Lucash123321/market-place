from django.test import TestCase, Client
from supplies.models import User, Supply, Comment, Message
from django.urls import reverse


class TestUrls(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.first_user = User.objects.create_user('first_user')
        cls.second_user = User.objects.create_user('second_user')
        cls.author = User.objects.create_user('author')

        data = {"user": cls.author,
                "name": f"Тестовый товар",
                "price": 999,
                "desc": "Тестовое описание"}
        supply = Supply.objects.create(**data)
        data = {"user": cls.author, "supply": supply, "rating": "5", "text": f"Тестовый комментарий"}
        Comment.objects.create(**data)

        cls.unauthorized_access = (
            reverse("supplies:index"),
            reverse("supplies:supply", kwargs={'id': 1}),
            reverse("supplies:profile", kwargs={'username': cls.second_user.username}),
        )

        cls.authorized_access = (
            reverse("supplies:add_supply"),
            reverse("supplies:messanger"),
            reverse("supplies:chat", kwargs={'username': cls.second_user.username}),
        )

        cls.author_access = (
            reverse("supplies:change_comment", kwargs={"id": 1}),
            reverse("supplies:change_supply", kwargs={"id": 1})
        )

    def setUp(self):
        self.first_user_client = Client()
        self.first_user_client.force_login(self.first_user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    def test_unauthorized_access(self):
        for url in self.unauthorized_access:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        for url in self.authorized_access:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

        for url in self.author_access:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

    def test_authorized_access(self):
        for url in self.unauthorized_access:
            response = self.first_user_client.get(url)
            self.assertEqual(response.status_code, 200)

        for url in self.authorized_access:
            response = self.first_user_client.get(url)
            self.assertEqual(response.status_code, 200)

        for url in self.author_access:
            response = self.first_user_client.get(url)
            self.assertEqual(response.status_code, 302)

    def test_author_access(self):
        for url in self.unauthorized_access:
            response = self.author_client.get(url)
            self.assertEqual(response.status_code, 200)

        for url in self.authorized_access:
            response = self.author_client.get(url)
            self.assertEqual(response.status_code, 200)

        for url in self.author_access:
            response = self.author_client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_wrong_url(self):
        response = self.client.get('something/really/weird')
        self.assertEqual(response.status_code, 404)
