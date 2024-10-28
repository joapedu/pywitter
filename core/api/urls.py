from django.urls import path
from .views import ExplorePostsView, PostListCreateView, LikePostView, FollowUserView, FeedView, PostSearchView, RegisterUserView, UnfollowUserView, UserInfoView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user-info/', UserInfoView, name='user-info'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('explore/', ExplorePostsView.as_view(), name='explore'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', PostSearchView.as_view(), name='search-posts'),
]
