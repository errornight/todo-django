from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from functools import wraps


def cookie_check(view_func):
    # a decorator to check request cookie.
    def wrapper(request, *args, **kwargs):
        user_id = request.COOKIES.get('user_id')
        if user_id:
            user = User.objects.get(public_id=user_id)
        else:
            user = User.objects.create()
            response = view_func(request, user, *args, **kwargs)
            response.set_cookie('user_id', user.public_id)
            return response

        return view_func(request, user, *args, **kwargs)

    return wrapper



@cookie_check
def home(request, user):
    context = {'user': user}
    return render(request, 'main/home.html', context)




