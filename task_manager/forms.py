from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class TailwindFormMixin:
    widget_class = 'block w-full'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.widget.is_hidden:
                continue

            current_class = field.widget.attrs.get('class', '')
            default_class = 'block' if current_class else self.widget_class
            field.widget.attrs['class'] = (
                f'{current_class} {default_class}'.strip()
            )


class LoginForm(TailwindFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = _('Username')
        self.fields['password'].label = _('Password')
