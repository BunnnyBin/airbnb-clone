from django import forms
from . import models

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_email(self):  #clean_해당 필드 : 해당 필드를 정리하는 기능 -> cleaned_data 안에서 확인 가능
    #     email = self.cleaned_data.get("email")  # self.cleaned_data : login에 작성한 email, 딕셔너리 형태
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")  # form안에 에러 만드는 방법

    def clean(self):  # self == form
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):  # user의 password를 체크하는 함수
                return self.cleaned_data  # email, password를 리턴
            else:
                # raise forms.ValidationError("Password is wrong") - 해당 password 필드에 에러가 안생기는 문제
                self.add_error("password", forms.ValidationError("Password is wrong")) # forms.add_error()
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))  # forms.add_error()

