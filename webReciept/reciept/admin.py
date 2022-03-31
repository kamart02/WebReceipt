from django.contrib import admin
from .models import Group, Item, Reciept, ItemInfo, Transaction

# Register your models here.
class RecieptAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'wholeCost')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('reciept', 'name', 'amount', 'price', 'cost')

admin.site.register(Reciept, RecieptAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Group)
admin.site.register(ItemInfo)

admin.site.register(Transaction)