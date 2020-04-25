from django.shortcuts import render
from django.views import View
from . import forms

class LoginView(View):
    def get(self, request):  # function : if request.method == "GET"
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form":form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # cleaned_data : form의 모든 필드를 정리해준 결과
        return render(request, "users/login.html", {"form":form})