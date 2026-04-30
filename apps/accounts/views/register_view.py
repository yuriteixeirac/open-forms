from django.contrib.auth import login
from apps.accounts.forms import RegisterForm
from django.shortcuts import render, redirect


def register_view(request):
    if request.method == 'GET':
        return render(request, 'accounts/register-form.html', context={
            'form': RegisterForm()
        })

    # TODO: implementar lógica de registro
    form = RegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'accounts/register-form.html', context={
            'form': form
        })

    user = form.save()
    login(request, user)

    return redirect('register-view')
