import os
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms, models


# class LoginView(View):
#     def get(self, request):  # function : if request.method == "GET"
#         form = forms.LoginForm()
#         return render(request, "users/login.html", {"form":form})
#
#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")  # cleaned_data : form의 모든 필드를 정리해준 결과
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password) # 인증
#             if user is not None:
#                 login(request, user) # 로그인해줌
#                 return redirect(reverse("core:home")) # reverse(name) : url로 전환됨
#         return render(request, "users/login.html", {"form":form})

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")  # 바로 실행하지 않고 필요할때 실행된다(views에서 urls이 불러지지 않으므로?)

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)  # success_url로 간다


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        'first_name': '김',
        'last_name': '유빈',
        'email': 'itn@naver.com'
    }

    def form_valid(self, form):
        form.save()
        # login
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

def complete_verification(request, key): # url.py의 <str:key>와 일치한 이름(key)
    try:
        user = models.User.objects.get(email_secret = key)
        user.email_verified = True
        user.email_secret = "" # 인증하고 삭제하기
        user.save()
        #todo : add success message
    except models.User.DoesNotExist:
        #todo : add error message
        pass
    return redirect(reverse("core:home"))

def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")

def github_callback(request):
    pass