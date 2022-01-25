import logging

from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger('users')


def login(request):
    if request.method == 'GET':
        return render(request, '../templates/users/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(authenticate, username=username, password=password)

        if user is not None:
            login_django(request, user)
            context = {'login_success': True}
            template = '../templates/base/base.html'
        else:
            context = {'login_success': False}
            template = '../templates/users/login.html'

    return render(request, template, context)


@login_required
def logout(request):
    logout_django(request)
    context = {'logout_success': True}
    return render(request, '../templates/base/base.html', context)


def home(request):
    return render(request, '../templates/base/base.html')
