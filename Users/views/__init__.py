import logging

from django.contrib.auth import authenticate, logout as logout_request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger('users')


def login(request):
    if request.method == 'GET':
        return render(request, '../templates/users/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        logger.error(username)
        logger.error(password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            context = {'login_success': False}
        else:
            context = {'login_success': True}

    logger.error(request.user.is_authenticated)
    return render(request, '../templates/users/login.html', context)


@login_required
def logout(request):
    logout_request(request)
    return render(request, '../templates/base/base.html')


def home(request):
    logger.error(request.user.is_authenticated)
    return render(request, '../templates/base/base.html')
