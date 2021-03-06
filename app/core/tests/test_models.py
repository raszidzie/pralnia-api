from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='testuser@gamil.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@gmail.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password), True)

    def test_new_user_email_normalized(self):
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(email, 'pass1234')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'pass123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'testpass1234'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)
    
    def test_clothes_str(self):
        clothe = models.Clothe.objects.create(
            user=sample_user(),
            name='Jumper'
        )

        self.assertEqual(str(clothe), clothe.name)

    def test_wash_str(self):
        wash = models.Wash.objects.create(
            user=sample_user(),
            title='Jumper',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(wash), wash.title)