# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Blog

# def post_list(request):
#     all_posts = Blog.objects.all()
#     return render(request, '../blog/home.html', {'posts': all_posts})