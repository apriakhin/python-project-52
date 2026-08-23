from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.forms import TailwindFormMixin

from .models import Label


class LabelForm(TailwindFormMixin, forms.ModelForm):
    name = forms.CharField(
        label=_('Name'),
        error_messages={
            'unique': _('A label with this name already exists.'),
        },
    )

    class Meta:
        model = Label
        fields = ['name']
