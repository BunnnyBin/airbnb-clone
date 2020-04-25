from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from . import forms

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
        return super().form_valid(form) # success_url로 간다

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
