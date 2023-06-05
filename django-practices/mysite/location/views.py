from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Load, Dumb
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse


def index(request):
    fh = open('loc.js')
    return render(request, 'location/index.html')


