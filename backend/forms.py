from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    role = forms.ChoiceField(
        choices=[('visitor', 'Посетитель'), ('master', 'Мастер')],
        label="Роль"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500"
            })

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={
                "min": 1, "max": 5,
                "class": "w-20 border rounded-lg px-2 py-1 focus:ring-2 focus:ring-green-500"
            }),
            "comment": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-green-500"
            }),
        }
