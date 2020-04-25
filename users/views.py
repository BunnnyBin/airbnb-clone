from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from . import forms

class LoginView(View):
    def get(self, request):  # function : if request.method == "GET"
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form":form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")  # cleaned_data : form의 모든 필드를 정리해준 결과
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password) # 인증
            if user is not None:
                login(request, user) # 로그인해줌
                return redirect(reverse("core:home")) # reverse(name) : url로 전환됨
        return render(request, "users/login.html", {"form":form})

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
