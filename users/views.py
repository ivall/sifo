from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from .models import User
from .utils import data_exist, hash_password, verify_password, verify_captcha
from .decorators import login_required


class UserCreate(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/signup.html')

    def post(self, request, *args, **kwargs):
        captcha = request.POST.get("g-recaptcha-response")

        if not verify_captcha(captcha):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/users/register')

        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not data_exist(username, password1, password2):
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/users/register')

        check_username = User.objects.filter(username=username)
        if check_username:
            messages.add_message(request, messages.ERROR, 'Użytkownik z takim loginem już istnieje.')
            return redirect('/users/register')

        if password1 != password2:
            messages.add_message(request, messages.ERROR, 'Hasła nie zgadzają się.')
            return redirect('/users/register')

        password = hash_password(password1).decode('utf-8')

        user = User(
            username=username,
            password=password
        )
        user.save()

        request.session['user_id'] = user.pk
        request.session['account_type'] = user.account_type

        messages.add_message(request, messages.SUCCESS, 'Zarejestrowano i zalogowano.')
        return redirect('/users/register')


class UserLogin(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/signin.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not data_exist(username, password):
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/users/login')

        user = User.objects.filter(username=username).values('id', 'password', 'account_type')
        if not user:
            messages.add_message(request, messages.ERROR, 'Taki użytkownik nie istnieje.')
            return redirect('/users/login')

        if not verify_password(password, user[0]['password']):
            messages.add_message(request, messages.ERROR, 'Hasło nie jest poprawne.')
            return redirect('/users/login')

        request.session['user_id'] = user[0]['id']
        request.session['account_type'] = user[0]['account_type']
        messages.add_message(request, messages.SUCCESS, 'Zalogowano.')
        return redirect('/')


class UserLogout(View):

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        del request.session['user_id']
        del request.session['account_type']
        messages.add_message(request, messages.SUCCESS, 'Wylogowano.')
        return redirect('/')


