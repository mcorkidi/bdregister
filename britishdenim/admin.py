from django.contrib import admin
from .models import Item, Consumer, Scan, Coupon
# Register your models here.

class ItemAdmin(admin.ModelAdmin):

    list_display = ('sku', 'name')


class ConsumerAdmin(admin.ModelAdmin):

    list_display = ('sku', 'user_id', 'where', 'when', 'country', 'city')

class ScanAdmin(admin.ModelAdmin):

    list_display = ('sku', 'where', 'when', 'country', 'city')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('issuer', 'creationDate', 'expirationDate')

admin.site.register(Item, ItemAdmin)
admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(Scan, ScanAdmin)
admin.site.register(Coupon, CouponAdmin)