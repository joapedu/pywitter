from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views import create_post_view, explorer_view, feed_view, login_view, register_view, user_view

schema_view = get_schema_view(
    openapi.Info(
        title="Pywitter",
        default_version='v1',
        description="The Pywitter Project Api",
        contact=openapi.Contact(email="joaoeduardobraga2@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('cadastro/', register_view, name='cadastro'),
    path('login/', login_view, name='login'),
    path('criar_post/', create_post_view, name='criar_post'),
    path('feed/', feed_view, name='feed'),
    path('explorar/', explorer_view, name='explorar'),
    path('usuario/', user_view, name='usuario'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)