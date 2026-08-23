from django.urls import path

from .views import CreateView, DeleteView, DetailView, IndexView, UpdateView


urlpatterns = [
    path('', IndexView.as_view(), name='tasks_index'),
    path('create/', CreateView.as_view(), name='tasks_create'),
    path('<int:pk>/', DetailView.as_view(), name='tasks_detail'),
    path('<int:pk>/update/', UpdateView.as_view(), name='tasks_update'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='tasks_delete'),
]
