from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class IndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class CreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_index')

    def form_valid(self, form):
        messages.success(self.request, _('Label successfully created'))
        return super().form_valid(form)


class UpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_index')

    def form_valid(self, form):
        messages.success(self.request, _('Label successfully updated'))
        return super().form_valid(form)


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    context_object_name = 'label'

    def form_valid(self, form):
        if self.get_object().task_set.exists():
            messages.error(self.request, _('Unable to delete label'))
            return redirect('labels_index')

        messages.success(self.request, _('Label successfully deleted'))
        return super().form_valid(form)
