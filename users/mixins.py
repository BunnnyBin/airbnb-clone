from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

#mixins - 가면 안되는 페이지에 주소를 입력하는 것만으로 접근가능하는 위험을 방지(특정 케이스만 뷰 실행하도록)
#로그아웃 한 사람(익명의 유저)만 볼 수 있다.
class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated #return true이면 view를 실행해준다.(view와url의 미들웨어같은 역할)

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect(reverse("core:home"))

class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login") # 로그인 안된 사람인 경우는 여기로 데려간다.

class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")


