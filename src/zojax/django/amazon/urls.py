import dselector

parser = dselector.Parser()

urlpatterns = parser.patterns('zojax.django.amazon.views',
    (r'books/{id:digits}-{slug:chunk}', 'view_book', {}, "view_book")
)

