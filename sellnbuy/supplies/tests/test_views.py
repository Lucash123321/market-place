from django.test import TestCase
from supplies.models import User, Supply
from django.urls import reverse


class TestView(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user('test')
        cls.post = Supply.objects.create(user=cls.user, name="Тестовое имя", price=10000)
        cls.used_templates = {
            reverse("supplies:index"): "supplies/index.html",
            reverse("supplies:add_supply"): "supplies/add_supply.html",
            reverse("supplies:messanger"): "supplies/messanger.html",
            reverse("supplies:supply", kwargs={'id': cls.post.id}): "supplies/supply_page.html",
            reverse("supplies:profile", kwargs={cls.user.username}): "supplies/profile.html",
            reverse("supplies:chat"): "supplies/chat.html"
        }

    def test_views_templates(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'supplies/index.html')

    def test_profile_page_temlate(self):
        user = User.objects.create_user('test')
        response = self.client.get('/test/')
        self.assertTemplateUsed(response, 'supplies/profile.html')
