from django import template

register = template.Library()

@register.filter(name='in_wishlist')
def in_wishlist(product, wishlist):
    return wishlist.filter(product__id=product.id).exists()