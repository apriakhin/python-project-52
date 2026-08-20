from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserCreationForm(UserCreationForm):
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

        self.order_fields(
            (
                'username',
                'first_name',
                'last_name',
                'password1',
                'password2',
            )
        )
