from amazonproduct import InvalidParameterValue
from zojax.django.amazon.settings import AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, \
    AMAZON_LOCALE, AMAZON_ASSOCIATE_TAG
import amazonproduct
import urllib


class ConfigurationError(Exception):
    pass


def item_lookup(amazon_id):
    if not AMAZON_ACCESS_KEY:
        raise ConfigurationError("You must specify a valid AMAZON_ACCESS_KEY in project settings")
    if not AMAZON_SECRET_KEY:
        raise ConfigurationError("You must specify a valid AMAZON_SECRET_KEY in project settings")
    api = amazonproduct.API(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_LOCALE)
    kw = {'ResponseGroup': 'Medium'}
    if AMAZON_ASSOCIATE_TAG:
        kw['AssociateTag'] = AMAZON_ASSOCIATE_TAG
    try:
        return api.item_lookup(amazon_id, **kw).Items.Item[0]
    except InvalidParameterValue:
        raise Exception("Invalid amazon ID")
    except:
        raise



def get_book_data(item):
    data = {}
    if item.ItemAttributes.ProductGroup != 'Book':
        raise Exception("This amazon ID does not refer to book product.")
    data['url'] = urllib.unquote(unicode(item.DetailPageURL))
    data['title'] = unicode(item.ItemAttributes.Title)
    for r in item.EditorialReviews.EditorialReview:
        if r.Source == 'Product Description':
            data['description'] = unicode(r.Content)
            break
    data['author'] = unicode(getattr(item.ItemAttributes, "Author", u''))
    try:
        data['small_image_url'] = unicode(item.SmallImage.URL)  
    except AttributeError:
        data['small_image_url'] = None
    try:
        data['medium_image_url'] = unicode(item.MediumImage.URL)  
    except AttributeError:
        data['medium_image_url'] = None
    try:
        data['large_image_url'] = unicode(item.LargeImage.URL)
    except AttributeError:
        data['large_image_url'] = None
    return data  
    