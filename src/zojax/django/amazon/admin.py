from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
from django.views.decorators.csrf import csrf_protect
from zojax.django.amazon.forms import BookAdminForm, BookAddForm, \
    BookSearchAdminForm
from zojax.django.amazon.models import Book, BookSearch
from zojax.django.categories.models import Category
from zojax.django.location.models import LocatedItem


class BookAdmin(admin.ModelAdmin):

    form = BookAdminForm
    
    list_display = ('amazon_id', 'title', 'author', 'published')
    list_editable = ('title', 'published',)
    list_filter = ('published',)
    
    search_fields = ('title', 'author', 'amazon_id',)
    
    fieldsets = (
            (None, {
                'classes': ('categories',),
                'fields': ('categories',)
            }),
            (None, {
                'fields': ('amazon_id', 'url', 'title', 'author', 'description',
                           'small_image_url', 'medium_image_url', 'large_image_url',
                           'published',)
            }),
        )

    def publish(self, request, queryset):
        count = 0
        for item in queryset:
            item.published = True
            item.save()
            count += 1
        self.message_user(request,
                          ungettext_lazy(u"%(count)d item was published",
                                         u"%(count)d items were published", count) 
                          % {'count': count})
    publish.short_description = _(u"Publish selected items")

    actions = ['publish']

    @csrf_protect
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for book model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        if request.method == 'POST':
            form = BookAddForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                amazon_id = data.pop('amazon_id')
                title = data.pop('title')
                url = data.pop('url') 
                new_object = self.model(amazon_id=amazon_id, title=title, url=url)
                for k, v in data.items():
                    setattr(new_object, k, v)
                new_object.save()
                self.log_addition(request, new_object)
                return self.response_add(request, new_object)
                
        else:
            form = BookAddForm()
        
        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'form': form,
            'media': "",
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        return render_to_response("admin/amazon/book/add.html", context,
                                  context_instance=RequestContext(request))


class BookSearchAdmin(admin.ModelAdmin):
    
    form = BookSearchAdminForm

    def save_model(self, request, obj, form, change):
        super(BookSearchAdmin, self).save_model(request, obj, form, change)
        Category.objects.update_categories(obj, form.cleaned_data['categories'])
        LocatedItem.objects.update(obj, form.cleaned_data['location'])
        
    fieldsets = (
            (None, {
                'classes': ('categories',),
                'fields': ('categories',)
            }),
            (None, {
                'classes': ('location',),
                'fields': ('location',)
            }),
            (None, {
                'fields': ('keywords', 'browse_node',)
            }),
        )

    def fetch(self, request, queryset):
        cnt = 0
        for search in queryset:
            cnt += search.fetch()
        self.message_user(request,
                          ungettext_lazy(u"%(count)d book was fetched",
                                         u"%(count)d books were fetched", cnt) 
                          % {'count': cnt})
    fetch.short_description = _(u"Harvest selected searches")

    actions = ['fetch']    


admin.site.register(Book, BookAdmin)
admin.site.register(BookSearch, BookSearchAdmin)
