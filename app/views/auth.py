from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from app.form import RegisterForm, LoginForm
from app.models import Cart





def my_account(request):
    return render(request=request,
                  template_name='app/pages_main/my_account.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    elif request.method == "POST":
        form = LoginForm(request=request,
                         data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(user=user,
                  request=request)

            return redirect('index')

    form = LoginForm()
    return render(request=request,
                  template_name='app/pages_main/login.html',
                  context={"form":form})


def register_page(request):
    if request.user.is_authenticated:
        return redirect("index")
    elif request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = RegisterForm()
    return render(request=request,
                  template_name='app/pages_main/register.html',
                  context={'form': form})


def logout_view(request):
    logout(request=request)
    return redirect('index')


