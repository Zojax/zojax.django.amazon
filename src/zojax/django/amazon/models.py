from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from zojax.django.amazon.settings import AMAZON_ASSOCIATE_TAG
from zojax.django.categories import register
from zojax.django.contentitem.models import ContentItem
import urllib2


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
        