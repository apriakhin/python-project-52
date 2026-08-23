from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from task_manager.forms import TailwindFormMixin

from .models import Task


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
    )
    executor = forms.ModelChoiceField(
        label=_('Executor'),
        queryset=get_user_model().objects.all(),
        required=False,
    )
    labels = forms.ModelMultipleChoiceField(
        label=_('Labels'),
        queryset=Label.objects.all(),
        required=False,
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
