from enum import auto
from django.db import models
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

# Create your models here.

class Group(models.Model):
    accounts = models.ManyToManyField(User)
    name = models.CharField (max_length = 25)

class GroupUserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    balances = models.ManyToManyField(User)

class balance

class Reciept(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    wholeCost = models.DecimalField(max_digits=9, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Item(models.Model):
    reciept = models.ForeignKey(Reciept, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=5)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    cost = models.DecimalField(max_digits=9, decimal_places=2, editable=False, default=0)
    payer = models.ManyToManyField(User, through = 'ItemInfo', blank=True)

class ItemInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
