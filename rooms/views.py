from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)  # Paginator object
    try:
        rooms = paginator.page(int(page))  # Page object
        return render(request, "rooms/all_rooms.html", context={
            "page": rooms,
        })
    except EmptyPage:  # except Exception : 모든 예외 발생
        rooms = paginator.page(1)
        return redirect("/")
