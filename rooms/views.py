from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView
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
        context = super().get_context_data(**kwargs) # rooms, page_obj를 context에 추가한다.
        now = timezone.now()
        context["now"] = now
        return context