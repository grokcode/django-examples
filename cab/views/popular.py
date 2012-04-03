from django.views.generic.list_detail import object_list
from cab.models import Snippet


def top_authors(request):
    return object_list(request,
                       queryset=Snippet.objects.top_authors(),
                       template_name='cab/top_authors.html',
                       paginate_by=20)
