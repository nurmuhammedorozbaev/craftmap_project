from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(
        choices=[('user', 'Пользователь'), ('master', 'Мастер')],
        label="Роль"
    )

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500"
            })
