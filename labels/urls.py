from django.urls import path

from .views import CreateView, DeleteView, IndexView, UpdateView

urlpatterns = [
    path('', IndexView.as_view(), name='labels_index'),
    path('create/', CreateView.as_view(), name='labels_create'),
    path('<int:pk>/update/', UpdateView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', DeleteView.as_view(), name='labels_delete'),
]
