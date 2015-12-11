# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def journal(request):
   return HttpResponse('<h1>Journal</h1>')