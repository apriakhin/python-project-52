from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.forms import TailwindFormMixin

from .models import Status


class StatusForm(TailwindFormMixin, forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        error_messages={
            'unique': _('A status with this name already exists.'),
        },
    )

    class Meta:
        model = Status
        fields = ['name']
