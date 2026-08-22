from django.urls import path
from .views import IndexView, CreateView, UpdateView, DeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='statuses_index'),
    path('create/', CreateView.as_view(), name='statuses_create'),
    path('<int:pk>/update/', UpdateView.as_view(), name='statuses_update'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='statuses_delete'),
]
