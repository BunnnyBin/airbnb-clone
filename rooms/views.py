from math import ceil
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)  # Paginator object
    rooms = paginator.get_page(page)  # Page object
    print(vars(rooms.paginator))
    return render(request, "rooms/all_rooms.html", context={
        "rooms":rooms,
    })
