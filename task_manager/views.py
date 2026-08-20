from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('You are logged in'))
        return response


class LogoutView(LogoutView):
    http_method_names = ['post']
    next_page = reverse_lazy('index')
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        messages.info(request, _('You are logged out'))
        return response
