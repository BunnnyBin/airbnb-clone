import os, requests
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models, mixins
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

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

class LoginView(mixins.LoggedOutOnlyView, FormView):
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
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    #form_class = UserCreationForm
    success_url = reverse_lazy("core:home")

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
                raise GithubException("Can't get access token")
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
                        raise GithubException(f"Please log in with {user.login_method}")
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
                        messages.success(request, f"Welcome back {user.first_name}")
                        return redirect(reverse("core:home"))

                else:  # 깃허브 계정이 없는 경우
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")

    except GithubException as e:
        messages.error(request, e)
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
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get("access_token")

        profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={'Authorization':f"Bearer {access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        if email is None:
            raise KakaoException("Please also give me your email")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url")

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
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
            if profile_image is not None:
                photo_request = requests.get(profile_image) # (이해x!)url로부터 request하기
                user.avatar.save(f"{nickname}-avatar", ContentFile(photo_request.content)) # content는 byte file, ContentFile은 의미없는 bullhshit파일을 파일로 변환
                # filefield는 알아서 저장됨
                print(user.avatar)
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))

class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["hello"] = "Gggg"
    #     return context

#UpdateView : form의 data 넣기, 검증
class UpdateProfileView(SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "Profile Update"

    # url로 pk를 넘기지 않으므로 필요한 객체를 가져와야 한다.
    def get_object(self, queryset=None):
        return self.request.user

    # #username = email을 넣기 위해
    # #self == user(model)
    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)

    #placeholder 변경
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder":"Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "FirstName"}
        form.fields["last_name"].widget.attrs = {"placeholder": "LastName"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["bio"].widget.attrs = {"placeholder":"Bio"}
        return form

class UpdatePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update-password.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current Password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "Confirm Password"}
        return form

    success_message = "Password Update"

    #success_url 대신에
    def get_success_url(self):
        return self.request.user.get_absolute_url()