from django import forms
from . import models

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):  #clean_해당 필드 : 해당 필드를 정리하는 기능 -> cleaned_data 안에서 확인 가능
        email = self.cleaned_data.get("email")  # self.cleaned_data : login에 작성한 email, 딕셔너리 형태
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")  # form안에 에러 만드는 방법

    def clean_password(self):
        print("clean pass")