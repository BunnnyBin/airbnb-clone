from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

def all_rooms(request):
    now = datetime.now()
    return HttpResponse(content=f"<h1>{now}<h1>")