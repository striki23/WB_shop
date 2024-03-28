from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from users.forms import MyLoginForm, RegisterForm, ProfileUserForm, PasswordChangeForm
from django.views.generic import CreateView, UpdateView, View
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin


class LoginUser(LoginView):
    form_class = MyLoginForm
    template_name = 'users/login.html'


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = 'success'
    success_message = "Пользователь с логином '%(username)s' успешно создан."


class ProfileUser(UpdateView):
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')