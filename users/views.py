import os, requests
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


def complete_verification(request, key):  # url.py의 <str:key>와 일치한 이름(key)
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  # 인증하고 삭제하기
        user.save()
        # todo : add success message
    except models.User.DoesNotExist:
        # todo : add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)

        if code is not None:
            # 깃허브에 requests를 보내서 access token을 얻을 것
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"})
            token_json = token_request.json()
            error = token_json.get("error", None)

            if error is not None:
                raise GithubException()
            else:
                acceess_token = token_json.get("access_token")
                # github api에 request를 보내서 user의 정보를 가져온다.
                profile_request = requests.get("https://api.github.com/user",
                                               headers={"Authorization": f"token {acceess_token}",
                                                        "Accept": "application/json"},
                                               )
                profile_json = profile_request.json()
                username = profile_json.get('login', None)

                if username is not None:
                    name = profile_json.get('name')
                    email = profile_json.get('email', None)
                    bio = profile_json.get('bio')
                    if bio is None:
                        bio = "None"

                    if email is None:  # 깃허브의 이메일을 public으로 등록하지 않은 경우
                        raise GithubException()
                    else:
                        try:
                            user = models.User.objects.get(email=email)
                            if user.login_method != models.User.LOGIN_GITHUB:
                                raise GithubException()  # password나 kakao로 계정있는 경우 에러
                        except models.User.DoesNotExist:  # signup
                            user = models.User.objects.create(
                                email=email, first_name=name, username=email, bio=bio,
                                login_method=models.User.LOGIN_GITHUB, email_verified=True
                            )
                            user.set_unusable_password()  # Marks the user as having no password set.
                            user.save()

                        login(request, user)
                        return redirect(reverse("core:home"))

                else:  # 깃허브 계정이 없는 경우
                    raise GithubException()
        else:
            raise GithubException()

    except GithubException:
        # todo: send error message
        return redirect(reverse("users:login"))

def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

class KakaoException(Exception):
    pass

def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")

        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")

        profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={'Authorization':f"Bearer {access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url")

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException()
        except models.User.DoesNotExist: # signup
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True
            )
            user.set_unusable_password()
            user.save()
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))