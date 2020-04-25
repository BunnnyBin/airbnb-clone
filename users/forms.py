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
                self.add_error("password", forms.ValidationError("Password is wrong"))  # forms.add_error()
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))  # forms.add_error()


# class SignUpForm(forms.Form):
#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
#
#     # form은 clean함수를 지나칠 때마다 데이터에 추가된다.
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email = email)
#             raise forms.ValidationError("User already exists with that email")
#         except models.User.DoesNotExist:
#             return email
#
#     def clean_password1(self):
#         password1 = self.cleaned_data.get("password1")
#         password = self.cleaned_data.get("password")  # password1을 clena하려고 할때 이미 password는 cleaned이다.
#
#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:
#             return password
#
#     # user 생성
#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")
#
#         user = models.User.objects.create_user(email, email, password) # create와 다른점은 password을 암호화해서 저장함
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()

# ModelForm - form과 model을 연결해서 일일이 field를 정할 필요를 줄여준다.
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password = self.cleaned_data.get("password")  # password1을 clena하려고 할때 이미 password는 cleaned이다.

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # ModelForm - save() override
    def save(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = super().save(commit=False) # commit=False : django object는 생성하지만 데이터베이스에는 올리지 않는다.
        user.username = email
        user.set_password(password)
        user.save()