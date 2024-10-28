from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Count, Sum, Q
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.cache import cache

from core.settings import CACHE_TTL
from .models import Post, Like, Follow
from .serializers import UserSerializer, PostSerializer
from rest_framework.pagination import PageNumberPagination


def register_view(request):
    return render(request, 'api/registro.html')

def login_view(request):
    return render(request, 'api/login.html')

def create_post_view(request):
    return render(request, 'api/criar_post.html')

def feed_view(request):
    return render(request, 'api/feed.html')

def explorer_view(request):
    return render(request, 'api/explorar.html')

def user_view(request):
    return render(request, 'api/user_info.html')

@api_view(['GET'])
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        posts_count = Post.objects.filter(author=user).count()
        followers_count = Follow.objects.filter(following=user).count()
        following_count = Follow.objects.filter(follower=user).count()

        total_likes = Post.objects.filter(author=user).annotate(num_likes=Count('like')).aggregate(total=Sum('num_likes'))['total']

        data = {
            'username': user.username,
            'posts_count': posts_count,
            'followers_count': followers_count,
            'following_count': following_count,
            'total_likes': total_likes or 0
        }

        return Response(data)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            return Response({"message": "Post curtido com sucesso."}, status=201)
        else:
            like.delete()
            return Response({"message": "Curtida removida."}, status=200)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_to_follow = User.objects.get(id=self.kwargs['user_id'])
        follower = request.user

        follow, created = Follow.objects.get_or_create(follower=follower, following=user_to_follow)

        if created:
            return Response({"message": f"Você começou a seguir {user_to_follow.username}."}, status=201)
        else:
            return Response({"message": f"Você já está seguindo {user_to_follow.username}."}, status=200)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user_to_unfollow = User.objects.get(id=self.kwargs['user_id'])
        follower = request.user

        follow_relation = Follow.objects.filter(follower=follower, following=user_to_unfollow)
        if follow_relation.exists():
            follow_relation.delete()
            return Response({"message": f"Você deixou de seguir {user_to_unfollow.username}."}, status=200)
        return Response({"message": f"Você não estava seguindo {user_to_unfollow.username}."}, status=400)

class FeedPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = FeedPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        cache_key = f"user_feed_{user_id}"
        cached_feed = cache.get(cache_key)

        if cached_feed:
            return cached_feed
        else:
            following_users = self.request.user.following.all().values_list('following_id', flat=True)
            posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
            cache.set(cache_key, posts, timeout=CACHE_TTL)
            return posts

class ExplorePostsView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "Usuário criado com sucesso."
        }, status=status.HTTP_201_CREATED)

class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Post.objects.filter(
            Q(content__icontains=query)
        ).distinct()
