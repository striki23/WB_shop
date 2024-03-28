from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from shop.templatetags.shop_tags import get_year


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Телефон', widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterForm(UserCreationForm):

    password1 = forms.CharField(
        label='Пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Подтверждение пароля', widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'phone_number',
            'male', 'date_birth', 'first_name',
            'last_name', 'password1'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@mail.ru'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7900000000'
            }),
            'male': forms.Select(attrs={'class': 'form-control'}),
            'date_birth': forms.SelectDateWidget(
                attrs={'class': 'form-control'},
                years=tuple(range(get_year()-100, get_year()-16))
            ),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].help_text = "Формат номера '+79999999999'"


class ProfileUserForm(forms.ModelForm):
    phone_number = username = forms.CharField(
        disabled=True,
        label='Телефон',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'email', 'phone_number',
            'male', 'date_birth', 'first_name',
            'last_name'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@mail.ru'
            }),
            'male': forms.Select(attrs={'class': 'form-control'}),
            'date_birth': forms.SelectDateWidget(
                attrs={'class': 'form-control'},
                years=tuple(range(get_year() - 100, get_year() - 16))
            ),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    new_password1 = forms.CharField(
        label='Новый пароль', widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    new_password2 = forms.CharField(
        label='Подтверждения пароля', widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
