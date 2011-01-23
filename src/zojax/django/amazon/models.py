from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from zojax.django.amazon.settings import AMAZON_ASSOCIATE_TAG, AMAZON_ACCESS_KEY, \
    AMAZON_SECRET_KEY, AMAZON_LOCALE
from zojax.django.categories import register
from zojax.django.contentitem.models import ContentItem
import amazonproduct
import urllib2
from django.utils.hashcompat import md5_constructor
from zojax.django.amazon.utils import get_book_data
from zojax.django.categories.models import Category
from django.contrib.sites.models import Site


class AmazonItem(ContentItem):
    
    amazon_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    
    small_image_url = models.URLField(max_length=300, null=True, blank=True)
    medium_image_url = models.URLField(max_length=300, null=True, blank=True)
    large_image_url = models.URLField(max_length=300, null=True, blank=True)

    url = models.URLField(max_length=300, unique=True)
    
    def get_absolute_url(self):
        return self.url 
    
    class Meta:
        abstract = True
    
    
class Book(AmazonItem):

    author = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        ordering = ["-published_on"]
        verbose_name = _(u"Book")
        verbose_name_plural = _(u"Books")
        
    @property
    def author_search_url(self):
        if not self.author:
            return None
        search_url = "http://www.amazon.com/s?ie=UTF8&sort=relevancerank&search-alias=books&ref_=ntt_at_ep_srch&field-author=%s" % urllib2.quote(self.author)
        if AMAZON_ASSOCIATE_TAG:
            search_url = "http://www.amazon.com/gp/redirect.html?ie=UTF8&location=%s&tag=%s&linkCode=ur2" % (urllib2.quote(search_url), urllib2.quote(AMAZON_ASSOCIATE_TAG))
        return search_url

    @permalink
    def get_absolute_url(self):
        return ('view_book', (self.id, self.slug)) 
        
register(Book)


class BookSearch(models.Model):

    keywords = models.CharField(max_length=100)
    browse_node = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.keywords
    
    class Meta:
        verbose_name = _("Book search")
        verbose_name_plural = _("Book searches")
        
    
    def fetch(self):
        cnt = 0
        
        if not AMAZON_ACCESS_KEY or not AMAZON_SECRET_KEY:
            return cnt
    
        api = amazonproduct.API(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_LOCALE)
        
        kw = {'ResponseGroup': 'Medium'}
        kw['Keywords'] = self.keywords
        kw['AssociateTag'] = AMAZON_ASSOCIATE_TAG
        if self.browse_node:
            kw['BrowseNode'] = str(self.browse_node)
        response = api.item_search('Books', **kw)
        for item in response.Items.Item:
            amazon_id = item.ASIN
            try:
                Book.objects.get(amazon_id=amazon_id)
                continue
            except Book.DoesNotExist:
                pass 
            try:
                data = get_book_data(item)
            except:
                continue
            book = Book(amazon_id=amazon_id)
            for field_name, value in data.items():
                if hasattr(book, field_name):
                    setattr(book, field_name, value)
            book.save()
            Category.objects.update_categories(book, self.categories)
            cnt += 1
            
        return cnt

register(BookSearch)
