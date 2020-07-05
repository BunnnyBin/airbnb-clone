from django.shortcuts import render
from django.db.models import Q
from users import models as user_models
from . import models

def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        #Q objects - complex queries(filter로 할 수 없는 경우)
        conversation = models.Conversation.objects.get(
            Q(participants=user_one) & Q(participants=user_two)
        )
