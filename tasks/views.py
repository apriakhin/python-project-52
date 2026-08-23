from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import TaskForm
from .models import Task


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.select_related(
            'author',
            'executor',
            'status',
        ).prefetch_related('labels')


class CreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _('Task successfully created'))
        return super().form_valid(form)


class UpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_index')

    def form_valid(self, form):
        messages.success(self.request, _('Task successfully updated'))
        return super().form_valid(form)


class DetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_index')
    context_object_name = 'task'

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('Only the task author can delete it'),
            )
            return redirect('tasks_index')

        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, _('Task successfully deleted'))
        return super().form_valid(form)
