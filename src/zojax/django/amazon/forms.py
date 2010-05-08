from django import forms
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from zojax.django.amazon.models import Book, BookSearch
from zojax.django.amazon.utils import get_book_data, item_lookup
from zojax.django.categories.forms import CategoriesField
from zojax.django.categories.models import Category
import sys
from zojax.django.location.forms import LocationChoiceField
from zojax.django.location.models import LocatedItem


class BookAddForm(forms.Form):

    amazon_id = forms.CharField(required=True)

    def clean(self):
        super(BookAddForm, self).clean()
        amazon_id = self.cleaned_data.get('amazon_id')
        instance = getattr(self, 'instance', None)
        if amazon_id or (instance and instance.amazon_id != amazon_id):
            try:
                item = item_lookup(amazon_id)
                self.cleaned_data.update(get_book_data(item))
            except Exception:
                self._errors["amazon_id"] = ErrorList([sys.exc_info()[1]])
                del self.cleaned_data["amazon_id"]
                return self.cleaned_data
        return self.cleaned_data


class BookAdminForm(ModelForm):

    categories = CategoriesField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(BookAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not instance.amazon_id:
            self.fields['title'].required = False
            self.fields['url'].required = False
        if instance and not self.fields['categories'].initial:
            self.fields['categories'].initial = Category.objects.get_for_object(instance)

    def _get_validation_exclusions(self):
        exclude = super(BookAdminForm, self)._get_validation_exclusions()
        exclude.append('title')
        exclude.append('url')
        return exclude 

    def clean(self):    
        super(BookAdminForm, self).clean()
        amazon_id = self.cleaned_data.get('amazon_id')
        instance = getattr(self, 'instance', None)
        if amazon_id or (instance and instance.amazon_id != amazon_id):
            try:
                self.cleaned_data.update(get_book_data(amazon_id))
            except Exception:
                self._errors["amazon_id"] = ErrorList([sys.exc_info()[1]])
                del self.cleaned_data["amazon_id"]
                return self.cleaned_data
        return self.cleaned_data
        
    def save(self, commit=True):
        instance = super(BookAdminForm, self).save(commit)
        Category.objects.update_categories(instance, self.cleaned_data['categories'])
        return instance
            
    class Meta:
        model = Book
        fields = ('categories', 'amazon_id', 'url', 'title', 'description',
                  'author', 'small_image_url', 'medium_image_url',
                  'large_image_url', 'published', )        


class BookSearchAdminForm(ModelForm):

    categories = CategoriesField(required=True)
    location = LocationChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(BookSearchAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and not self.fields['categories'].initial:
            self.fields['categories'].initial = Category.objects.get_for_object(instance)
        if instance and not self.fields['location'].initial:
            self.fields['location'].initial = LocatedItem.objects.get_for_object(instance)

    class Meta:
        model = BookSearch
        fields = ('categories', 'keywords', 'browse_node', )
