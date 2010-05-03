from django.contrib.sitemaps import Sitemap
from zojax.django.amazon.models import Book


class BooksSitemap(Sitemap):
    
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Book.objects.all()
        