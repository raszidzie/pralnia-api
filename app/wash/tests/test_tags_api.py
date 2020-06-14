from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from wash.serializers import TagSerializer

TAGS_URL = reverse('wash:tag-list')

class PublicTagsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'paassword123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name="Jumper")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'testing@mail.com',
            'pass0987'
        )
        Tag.objects.create(user=user2, name="Jacket")
        tag = Tag.objects.create(user=self.user, name="Jumper")
        
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)