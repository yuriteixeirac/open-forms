from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from apps.accounts.forms import LoginForm


def login_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/login-form.html', context={
            'form': LoginForm()
        })

    form = LoginForm(request.POST)

    if not form.is_valid():
        return render(request, 'accounts/login-form.html', context={
            'form': form
        })

    email, password = form.cleaned_data.values()

    user = authenticate(
        request,
        email=email,
        password=password
    )

    if not user:
        form.add_error(None, 'E-mail or password passed are invalid.')
        return render(request, 'accounts/login-form.html', context={
            'form': form
        })

    login(request, user)
    return HttpResponse('PASSED!!')
