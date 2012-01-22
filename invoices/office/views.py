#coding: utf-8

from seautils.views.decorators import render_with

@render_with('office/index.html')
def index(request):
    return {}
