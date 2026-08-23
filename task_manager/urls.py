from django.contrib import admin
from django.urls import path, include
from .views import IndexView, LoginView, LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', include('users.urls')),
    path('statuses/', include('statuses.urls')),
    path('labels/', include('labels.urls')),
    path('tasks/', include('tasks.urls')),
    path('admin/', admin.site.urls),
]
