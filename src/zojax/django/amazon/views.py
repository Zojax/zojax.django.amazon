from django.http import HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from zojax.django.amazon.models import Book


def view_book(request, id, slug):
    try:
        book = Book.objects.get(pk=int(id))
    except Book.DoesNotExist:
        raise Http404()
    if not book.published:
        raise Http404()
    if book.slug != slug:
        return HttpResponsePermanentRedirect(book.get_absolute_url())
    return render_to_response("amazon/book.html", {'book': book},
                              context_instance=RequestContext(request))