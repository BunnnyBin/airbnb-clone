from math import ceil
from django.http import Http404
from django_countries import countries
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, UpdateView
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users import mixins as user_mixins
from . import models, forms


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
    paginate_by = 12
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


# room 검색바 - 함수기반 view

# def search(request):
#     # city = request.GET.get("city", "Anywhere")  # 아무것도 검색 안 할시 = Anywhere
#     # city = str.capitalize(city)
#     # country = request.GET.get("country", "KR")
#     # room_type = int(request.GET.get("room_type", 0))
#     # price = int(request.GET.get("price", 0))
#     # guests = int(request.GET.get("guests", 0))
#     # bedrooms = int(request.GET.get("bedrooms", 0))
#     # beds = int(request.GET.get("beds", 0))
#     # baths = int(request.GET.get("baths", 0))
#     # instant = bool(request.GET.get("instant", 0))
#     # superhost = bool(request.GET.get("superhost", 0))
#     # s_amenities = request.GET.getlist("amenities")
#     # s_facilities = request.GET.getlist("facilities")
#     #
#     # # form에서 받은 값
#     # form = {
#     #     "city": city,
#     #     "s_room_type": room_type,
#     #     "s_country": country,
#     #     "price": price,
#     #     "guests": guests,
#     #     "bedrooms": bedrooms,
#     #     "beds": beds,
#     #     "baths": baths,
#     #     "s_amenities": s_amenities,
#     #     "s_facilities": s_facilities,
#     #     "instant": instant,
#     #     "superhost": superhost,
#     # }
#     #
#     # room_types = models.RoomType.objects.all()
#     # amenities = models.Amenity.objects.all()
#     # facilities = models.Facility.objects.all()
#     #
#     # # form으로 넘기는 값
#     # choices = {
#     #     "countries": countries,
#     #     "room_types": room_types,
#     #     "amenities": amenities,
#     #     "facilities": facilities,
#     # }
#     #
#     # #조건부 필터 - 검색 결과
#     # filter_args = {}
#     #
#     # if city != "Anywhere":
#     #     filter_args["city__startswith"] = city
#     #
#     # filter_args["country"] = country
#     #
#     # if room_type != 0:
#     #     filter_args["room_type__pk"] = room_type
#     #
#     # if price != 0:
#     #     filter_args["price__lte"] = price
#     #
#     # if guests != 0:
#     #     filter_args["guests__lte"] = guests
#     #
#     # if bedrooms != 0:
#     #     filter_args["bedrooms __lte"] = bedrooms
#     #
#     # if beds != 0:
#     #     filter_args["beds __lte"] = beds
#     #
#     # if baths != 0:
#     #     filter_args["baths __lte"] = baths
#     #
#     # if instant:
#     #     filter_args["instant_book"] = True
#     #
#     # if superhost:
#     #     filter_args["host__superhost"] = True
#     #
#     # if len(s_amenities) > 0:
#     #     for s_amenity in s_amenities:
#     #         rooms = rooms.filter(amenities__pk=int(s_amenity))
#     #
#     # if len(s_facilities) > 0:
#     #     for s_facility in s_facilities:
#     #         rooms = rooms.filter(facilities__pk=int(s_facility)
#     #
#     # rooms = models.Room.objects.filter(**filter_args)
#
#     country = request.GET.get("country")
#
#     if country:
#         form = forms.SearchForm(request.GET)  # form 안의 데이터
#         if form.is_valid():  # form안의 데이터가 에러가 없으면
#             print(form.cleaned_data)  # form의 데이터를 본다
#             city = form.cleaned_data.get("city")
#             country = form.cleaned_data.get("country")
#             room_type = form.cleaned_data.get("room_type")
#             price = form.cleaned_data.get("price")
#             guests = form.cleaned_data.get("guests")
#             bedrooms = form.cleaned_data.get("bedrooms")
#             beds = form.cleaned_data.get("beds")
#             baths = form.cleaned_data.get("baths")
#             instant_book = form.cleaned_data.get("instant_book")
#             superhost = form.cleaned_data.get("superhost")
#             amenities = form.cleaned_data.get("amenities")
#             facilities = form.cleaned_data.get("facilities")
#
#             filter_args = {}
#
#             if city != "Anywhere":
#                 filter_args["city__startswith"] = city
#
#             filter_args["country"] = country
#
#             if room_type is not None:
#                 filter_args["room_type"] = room_type
#
#             if price is not None:
#                 filter_args["price__lte"] = price
#
#             if guests is not None:
#                 filter_args["guests__lte"] = guests
#
#             if bedrooms is not None:
#                 filter_args["bedrooms __lte"] = bedrooms
#
#             if beds is not None:
#                 filter_args["beds __lte"] = beds
#
#             if baths is not None:
#                 filter_args["baths __lte"] = baths
#
#             if instant_book is True:
#                 filter_args["instant_book"] = True
#
#             if superhost is True:
#                 filter_args["host__superhost"] = True
#
#             for amenity in amenities:
#                 filter_args["amenities"] = int(amenity)
#
#             for facility in facilities:
#                 filter_args["facilities"] = int(facility)
#
#             rooms = models.Room.objects.filter(**filter_args)
#
#     else:
#         form = forms.SearchForm()  # 시작 폼
#
#     return render(request,
#                   "rooms/search.html",
#                   {"form": form, "rooms": rooms})

# class 기반 view
class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)  # form 안의 데이터
            if form.is_valid():  # form안의 데이터가 에러가 없으면
                #print(form.cleaned_data)  # form의 데이터를 본다 - {'city': 'Anywhere', 'country': 'KR', 'room_type': None, 'price': None, 'guests': None, 'bedrooms': None, 'beds': None,'baths': None, 'instant_book': False, 'superhost': False, 'amenities': <QuerySet [<Amenity: washing machine>, <Amenity:Balcony>, <Amenity: Bed Linen>]>, 'facilities': <QuerySet []>}
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__lte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms __lte"] = bedrooms

                if beds is not None:
                    filter_args["beds __lte"] = beds

                if baths is not None:
                    filter_args["baths __lte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                q_rooms = models.Room.objects.all()

                for amenity in amenities:
                    q_rooms = q_rooms.filter(amenities__pk = amenity.pk)  # amenities : <QuerySet [<Amenity: En suite bathroom>, <Amenity: Free Parking>, <Amenity: Freezer>]>

                for facility in facilities:
                    q_rooms = q_rooms.filter(facilities__pk = facility.pk)

                # print(request.GET) -> <QueryDict: {'city': ['Anywhere'], 'country': ['KR'], 'room_type': [''], 'price': [''], 'guests': [''], 'bedrooms': [''], 'beds': [''], 'baths': [''], 'amenities': ['3', '6', '9']}>
                #urlencode() : string으로 암호화

                #qs = models.Room.objects.filter(**filter_args).order_by("-created")
                qs = q_rooms.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5) # 묶음 단위/Paginator라는 객체가 생성
                #print(paginator) -> <django.core.paginator.Paginator object at 0x000001F1A9AF3910>
                page = request.GET.get("page", 1) # 요구 페이지
                rooms = paginator.get_page(page) # 페이지에 보여질 objects들을 queryset 형태로 반환

                return render(request,
                              "rooms/search.html",
                              {"form": form, "rooms": rooms})

        else:
            form = forms.SearchForm()  # 시작 폼

        return render(request, "rooms/search.html", {"form": form})

#UpdateView를 사용해서 model, field, template_name만 정하면 끝
class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):
    model = models.Room # model == queryset, url pk와 연동됨
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    #host가 아닌 사람이 룸을 수정하는 것을 방지함
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

#RoomDetail view이지만 host만 접속가능하고 사진이 보여질 것
class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):
    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room

@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.get(pk=photo_pk).delete() # delete() : 해당 queryset를 삭제
            messages.success(request, "Photo Deleted")
        return redirect(reverse("rooms:photos", kwargs={'pk':room_pk}))
    except models.Room.DoesNotExist:
        return redirect(revese("core:home"))

