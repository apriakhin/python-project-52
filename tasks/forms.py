from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from task_manager.forms import TailwindFormMixin

from .models import Task


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return user.get_full_name() or user.username


class TaskForm(TailwindFormMixin, forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        error_messages={
            'unique': _('A task with this name already exists.'),
        },
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea,
    )
    status = forms.ModelChoiceField(
        label=_('Status'),
        queryset=Task._meta.get_field('status').related_model.objects.all(),
        empty_label=_('Not selected'),
    )
    executor = UserChoiceField(
        label=_('Executor'),
        queryset=get_user_model().objects.all(),
        required=False,
        empty_label=_('Not selected'),
    )
    labels = forms.ModelMultipleChoiceField(
        label=_('Labels'),
        queryset=Label.objects.all(),
        required=False,
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class TaskFilterForm(TailwindFormMixin, forms.Form):
    status = forms.ModelChoiceField(
        label=_('Status'),
        queryset=Task._meta.get_field('status').related_model.objects.all(),
        required=False,
        empty_label=_('Not selected'),
        widget=forms.Select(attrs={'class': 'w-60'}),
    )
    executor = UserChoiceField(
        label=_('Executor'),
        queryset=get_user_model().objects.all(),
        required=False,
        empty_label=_('Not selected'),
        widget=forms.Select(attrs={'class': 'w-72'}),
    )
    label = forms.ModelChoiceField(
        label=_('Label'),
        queryset=Label.objects.all(),
        required=False,
        empty_label=_('Not selected'),
        widget=forms.Select(attrs={'class': 'w-56'}),
    )
    self_tasks = forms.BooleanField(
        label=_('Only own tasks'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4'}),
    )
