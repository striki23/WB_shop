from django import forms
from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth import get_user_model


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(
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


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин', widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        label='Электронная почта', widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    first_name = forms.CharField(
        label='Имя', widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    last_name = forms.CharField(
        label='Фамилия', widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
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
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password']

    def clean_email(self):
        cd_email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=cd_email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже зарегистрирован!')
        return cd_email

