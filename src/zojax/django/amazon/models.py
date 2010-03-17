from django.db import models
from django.utils.translation import ugettext_lazy as _
from zojax.django.contentitem.models import ContentItem
from zojax.django.categories import register


class AmazonItem(ContentItem):
    
    amazon_id = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    
    small_image_url = models.URLField(max_length=300, null=True, blank=True)
    medium_image_url = models.URLField(max_length=300, null=True, blank=True)
    large_image_url = models.URLField(max_length=300, null=True, blank=True)
    
    url = models.URLField(max_length=300, unique=True)
    
    @property
    def associate_url(self):
        return self.url
    
    class Meta:
        abstract = True
    
    
class Book(AmazonItem):

    author = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        ordering = ["-published_on"]
        verbose_name = _(u"Book")
        verbose_name_plural = _(u"Books")
        
        
register(Book)
        