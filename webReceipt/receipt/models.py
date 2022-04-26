from enum import auto
from django.db import models
from django.contrib.auth.models import GroupManager, User
from django.forms.models import modelformset_factory
import decimal

# Create your models here.

class Group(models.Model):
    accounts = models.ManyToManyField(User)
    name = models.CharField (max_length = 25)

    def __str__(self):
        return "Group {}".format(self.name)


class Transaction(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name = 'sender', on_delete=models.CASCADE)
    recipiant = models.ForeignKey(User, related_name = 'recipiant', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class Receipt(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    #wholeCost = models.DecimalField(max_digits=25, decimal_places=2, default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def wholeCost(self):
        items = self.item_set.all()

        wholeCost = decimal.Decimal(0)

        for item in items:
            wholeCost += item.cost

        return wholeCost


class Item(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=5)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    #cost = models.DecimalField(max_digits=22, decimal_places=2, editable=False, default=0)

    @property
    def cost(self):
        return self.price * self.amount

        

class ItemInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    #cost = models.DecimalField(max_digits=22, decimal_places=2, default=0)

    @property
    def cost(self):
        return self.item.price * self.amount
