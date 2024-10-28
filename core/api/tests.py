from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Follow, Like

class PostTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.login(username='user1', password='password')

    def test_create_post(self):
        response = self.client.post('/api/posts/', {'content': 'This is a test post'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_like_post(self):
        post = Post.objects.create(content='Test post', author=self.user1)
        response = self.client.post(f'/api/posts/{post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_follow_user(self):
        response = self.client.post(f'/api/users/{self.user2.id}/follow/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_feed(self):
        post = Post.objects.create(content='User2 post', author=self.user2)
        Follow.objects.create(follower=self.user1, following=self.user2)
        response = self.client.get('/api/feed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'User2 post')

    def test_pagination(self):
        for i in range(15):
            Post.objects.create(content=f'Post {i}', author=self.user1)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
