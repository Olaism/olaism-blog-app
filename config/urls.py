from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from users.views import UserDetailView

urlpatterns = [
    path('admin-panel-dashboard/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('posts/', include('posts.urls')),
    path('api/', include('posts.api.urls')),
    path('<slug:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('', include('pages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)