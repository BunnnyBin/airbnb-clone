from math import ceil
from django_countries import countries
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import Http404
from . import models


# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)  # Paginator object
#     try:
#         rooms = paginator.page(int(page))  # Page object
#         return render(request, "rooms/all_rooms.html", context={
#             "page": rooms,
#         })
#     except EmptyPage:  # except Exception : 모든 예외 발생
#         rooms = paginator.page(1)
#         return redirect("/")

class HomeView(ListView):
    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # rooms, page_obj를 context에 추가한다.
        now = timezone.now()
        context["now"] = now
        return context


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()

class RoomDetail(DetailView):
    # view한테 우리가 무슨 model를 원하는지 알려줘야함
    model = models.Room


# room 검색바
def search(request):
    city = request.GET.get("city", "Anywhere")  # 아무것도 검색 안 할시 = Anywhere
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    s_amenities = request.GET.get("amenities")
    s_facilities = request.GET.get("facilities")

    # form에서 받은 값
    form = {
        "city": city,
        "s_room_type": room_type,
        "s_country": country,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities":s_amenities,
        "s_facilities":s_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # form으로 넘기는 값
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities":amenities,
        "facilities":facilities,
    }

    return render(request,
                  "rooms/search.html",
                  {**form, **choices})
