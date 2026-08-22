from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from task_manager.forms import TailwindFormMixin


class UserCreationForm(TailwindFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = _('Username')
        self.fields['first_name'].label = _('First name')
        self.fields['last_name'].label = _('Last name')
        self.fields['password1'].label = _('Password')
        self.fields['password2'].label = _('Password confirmation')

        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['first_name'].widget.attrs.update(
            {
                'autocomplete': 'given-name',
                'autofocus': True,
            }
        )
        self.fields['last_name'].widget.attrs['autocomplete'] = 'family-name'

        self.order_fields(
            (
                'first_name',
                'last_name',
                'username',
                'password1',
                'password2',
            )
        )
