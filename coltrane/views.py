from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from coltrane.models import Entry, Category


def entries_index(request):
    return render_to_response('coltrane/entry_index.html',
                              { 'entry_list': Entry.live() })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return object_list(request, queryset=category.live_entry_set(),
                       extra_context={'category': category },
                       template_name='coltrane/category_detail.html')

