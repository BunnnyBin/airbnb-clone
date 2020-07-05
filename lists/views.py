from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from django.views.generic import TemplateView
from . import models

#list에 room 추가/삭제
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        #get은 하나의 Object만 찾아서 두개 이상이면 에러가 난다. -> OneToOneField models
        #created - for unpack tuple
        the_list, created = models.List.objects.get_or_create(user=request.user, name="My Favorite Houses")

        if action == 'add':
            the_list.rooms.add(room)
        elif action == 'remove':
            the_list.rooms.remove(room)

    return redirect(reverse("rooms:detail", kwargs={"pk":room_pk}))

class SeeFavsView(TemplateView):
    template_name = "lists/list_detail.html"


