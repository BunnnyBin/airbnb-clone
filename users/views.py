from django.shortcuts import render
from django.views import View
from . import forms

class LoginView(View):
    def get(self, request):  # function : if request.method == "GET"
        form = forms.LoginForm()
        return render(request, "users/login.html", {"form":form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
