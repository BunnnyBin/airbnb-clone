from django.shortcuts import render
from django.views import View

class LoginView(View):
    def get(self, request):  # function : if request.method == "GET"
        return render(request, "users/login.html")

    def post(self, request):
        pass
