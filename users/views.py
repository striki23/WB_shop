from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from users.forms import MyLoginForm, RegisterForm


class LoginUser(LoginView):
    form_class = MyLoginForm
    template_name = 'users/login.html'

    # def get_success_url(self):
    #     return reverse_lazy('shop:index')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_success.html')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

