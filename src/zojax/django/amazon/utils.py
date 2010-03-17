from zojax.django.amazon.settings import AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, \
    AMAZON_LOCALE, AMAZON_ASSOCIATE_TAG
import amazonproduct
from amazonproduct import InvalidParameterValue


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


def get_book_data(amazon_id):
    item = item_lookup(amazon_id)
    data = {}
    if item.ItemAttributes.ProductGroup != 'Book':
        raise Exception("This amazon ID does not refer to book product.")
    data['url'] = unicode(item.DetailPageURL)
    data['title'] = unicode(item.ItemAttributes.Title)
    for r in item.EditorialReviews.EditorialReview:
        if r.Source == 'Product Description':
            data['description'] = unicode(r.Content)
            break
    data['author'] = unicode(getattr(item.ItemAttributes, "Author", u''))
    data['small_image_url'] = unicode(item.SmallImage.URL)  
    data['medium_image_url'] = unicode(item.MediumImage.URL)  
    data['large_image_url'] = unicode(item.LargeImage.URL)
    return data  
    