# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator
# Create your views here.
from .models import Blog

def post_list(request):
    all_posts = Blog.objects.all()
    p = Paginator(all_posts, 5)     #5 is the size of the content on each page
    page_no = request.GET.get('page', 1)
    page = p.page(page_no)       #1 is the page I want to display
    return render(request, 'allPosts.html', {'posts': page})

