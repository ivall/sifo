from django.contrib import messages
from django.shortcuts import redirect

def login_required():
    def decorator(function):
        def wrapper(request, *args, **kw):
            if not 'user_id' in request.session:
                messages.add_message(request, messages.ERROR, 'Nie jesteś zalogowany.')
                return redirect('/')
            return function(request, *args, **kw)
        return wrapper
    return decorator


def admin_required():
    def decorator(function):
        def wrapper(request, *args, **kw):
            if request.session['account_type'] != 'admin':
                messages.add_message(request, messages.ERROR, 'Brak uprawnień.')
                return redirect('/')
            return function(request, *args, **kw)
        return wrapper
    return decorator