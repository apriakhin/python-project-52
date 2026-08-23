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

from .forms import TaskFilterForm, TaskForm
from .models import Task


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_filter_form(self):
        return TaskFilterForm(self.request.GET or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.get_filter_form()
        return context

    def get_queryset(self):
        queryset = Task.objects.select_related(
            'author',
            'executor',
            'status',
        ).prefetch_related('labels')
        filter_form = self.get_filter_form()

        if not filter_form.is_valid():
            return queryset

        if status := filter_form.cleaned_data['status']:
            queryset = queryset.filter(status=status)
        if executor := filter_form.cleaned_data['executor']:
            queryset = queryset.filter(executor=executor)
        if label := filter_form.cleaned_data['label']:
            queryset = queryset.filter(labels=label)
        if filter_form.cleaned_data['self_tasks']:
            queryset = queryset.filter(author=self.request.user)

        return queryset.distinct()


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
