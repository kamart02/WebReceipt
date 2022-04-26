from django.contrib import admin
from .models import Group, Item, Receipt, ItemInfo, Transaction

# Register your models here.
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'wholeCost')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'name', 'amount', 'price', 'cost')

admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Group)
admin.site.register(ItemInfo)

admin.site.register(Transaction)