from enum import auto
from django.db import models
from django.contrib.auth.models import GroupManager, User
from django.forms.models import modelformset_factory

# Create your models here.

class Group(models.Model):
    accounts = models.ManyToManyField(User)
    name = models.CharField (max_length = 25)

    def __str__(self):
        return "Group {}".format(self.name)

class BalanceInfo(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    user = models.ForeignKey(User, related_name = 'primary', on_delete=models.CASCADE)
    group = models.ForeignKey(Group,  on_delete=models.CASCADE)
    userTo = models.ForeignKey(User, related_name = 'to', on_delete=models.CASCADE)

    def __str__(self):
        return "Group {}, {} to {}".format(self.groupUserProfile.group.name, self.groupUserProfile.user.username, self.userTo.username)

class Transaction(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name = 'sender', on_delete=models.CASCADE)
    recipiant = models.ForeignKey(User, related_name = 'recipiant', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

class Reciept(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    wholeCost = models.DecimalField(max_digits=25, decimal_places=2)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __updateWholeCost(self):
        items = self.item_set.all()

        self.wholeCost = 0.0

        for item in items:
            self.wholeCost += item.cost

    def save(self, *args, **kwargs):
        self.__updateWholeCost()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        recieptInfos = self.recieptinfo_set.all()

        for recieptInfo in recieptInfos:
            ownerBalance = self.owner.balanceinfo_set.get(userTo = recieptInfo.user, group = self.group)
            userBalance = self.group.balanceinfo_set.get(user = recieptInfo.user, userTo = self.owner)
            ownerBalance.amount += recieptInfo.amount
            userBalance.amount -+ recieptInfo.amount

            userBalance.save()
            ownerBalance.save()

        super().delete(*args, **kwargs)


class RecieptInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reciept = models.ForeignKey(Reciept, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __updateAmount(self, *args, **kwargs):
        items = self.reciept.item_set.all()
        
        self.cost = 0
        for item in items:
            itemInfo = item.iteminfo_set.get(user = self.user)
            self.cost += itemInfo.cost
    
    def save(self, *args, **kwargs):
        self.__updateAmount()
        
        super().save(*args, **kwargs)
        
        

class Item(models.Model):
    reciept = models.ForeignKey(Reciept, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=5)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    cost = models.DecimalField(max_digits=22, decimal_places=2, editable=False, default=0)
    payer = models.ManyToManyField(User, through = 'ItemInfo', blank=True)

    def save(self, *args, **kwargs):
        self.cost = self.price * self.amount

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        itemInfos = self.iteminfo_set.all()

        super().delete(*args, **kwargs)
        

class ItemInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    cost = models.DecimalField(max_digits=22, decimal_places=2, default=0)


    def __updateCost(self, *argg, **kwargs):
        self.cost = self.amount * self.item.price

    def save(self, *args, **kwargs):
        self.__updateCost()

        super().save(*args, **kwargs)
