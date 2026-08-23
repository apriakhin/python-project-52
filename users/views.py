from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.deletion import ProtectedError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm


class IndexView(ListView):
    template_name = 'users/index.html'
    model = get_user_model()
    context_object_name = 'users'


class CreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, _('User successfully registered'))
        return super().form_valid(form)


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('You do not have permission to edit this user'),
            )
            return redirect('users_index')

        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, _('User successfully updated'))
        return super().form_valid(form)


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('You do not have permission to delete this user'),
            )
            return redirect('users_index')

        return super().handle_no_permission()

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, _('Unable to delete user'))
            return redirect('users_index')

        messages.success(self.request, _('User successfully deleted'))
        return response
