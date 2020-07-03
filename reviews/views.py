from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from . import forms

#데이터를 입력 받아서 검증 (validation)
#검증 성공 시 : 해당 데이터를 저장하고 success URL로 이동
#검증 실패 시 : 오류 메시지와 함께 입력폼을 다시 보여준다
def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST) #form 변수에 데이터를 준다
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))

        # form의 모든 validators(각 필드의 유효성 검사 함수) 호출 유효성 검증 수행
        # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
        # 검증에 실패시 form.error 에 오류 정보를 저장
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()  #이때서야 데이터베이스에 저장
            messages.success(request, "Room reviewed")
            return redirect(reverse("rooms:detail", kwargs={"pk":room.pk}))

