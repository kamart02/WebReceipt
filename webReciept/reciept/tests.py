from django.test import TestCase
from django.contrib.auth.models import User
import gruut_ipa
from .models import *

# Create your tests here.
class RecieptTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username = 'tester1', password = '123456789Abc!')
        self.u2 = User.objects.create(username = 'tester2', password = '!Abc123456789')
        self.u3 = User.objects.create(username = 'tester3', password = 'Abc!123456789')
        
        self.group1 = Group.objects.create(name = '1+2+3')
        self.group1.accounts.add(self.u1, self.u2, self.u3)
        
    def test_reciept_creation_with_items(self):
        reciept = Reciept.objects.create(group = self.group1, owner = self.u1)

        sum = 0

        for i in range(1,5):
            item = Item.objects.create(reciept = reciept, name = str(i) + 'Item', amount = i, price = i + 2)
            self.assertEqual(item.cost, i*(i+2))
            sum+=item.cost

        reciept.save()
        self.assertEqual(reciept.wholeCost, sum)

    def test_reciept_existance(self):
        self.test_reciept_creation_with_items()
        self.assertIsNotNone(Reciept.objects.get(owner = self.u1))

    def test_itemInfo_and_recieptInfo(self):
        self.test_reciept_creation_with_items()
        reciept = Reciept.objects.get(owner = self.u1)

        items = reciept.item_set.all()

        ii2_1 = ItemInfo.objects.create(user = self.u2, item = items[0], amount = 1)
        ii2_2 = ItemInfo.objects.create(user = self.u2, item = items[1], amount = 1)
        self.assertEqual(ii2_1.cost, 3)
        self.assertEqual(ii2_2.cost, 4)

        ii3_2 = ItemInfo.objects.create(user = self.u3, item = items[1], amount = 1)
        ii3_3 = ItemInfo.objects.create(user = self.u3, item = items[2], amount = 2)
        self.assertEqual(ii3_2.cost, 4)
        self.assertEqual(ii3_3.cost, 2*5)

        ri2 = RecieptInfo.objects.create(user = self.u2, reciept = reciept)
        ri3 = RecieptInfo.objects.create(user = self.u3, reciept = reciept)

        ri2.save()
        ri3.save()

        self.assertEqual(ri2.cost, 3 + 4)
        self.assertEqual(ri3.cost, 4+2*5)

        u2u1, _ = BalanceInfo.objects.get_or_create(user = self.u2, userTo = self.u1, group = reciept.group)
        u3u1, _ = BalanceInfo.objects.get_or_create(user = self.u3, userTo = self.u1, group = reciept.group)

        self.assertEqual(u2u1.amount, 3 + 4)
        self.assertEqual(u3u1.amount, 4+2*5)


    def test_balance_change_after_itemInfo_change(self):
        self.test_itemInfo_and_recieptInfo()

        reciept = Reciept.objects.get(owner = self.u1)
        items = reciept.item_set.all()

        u2u1, _ = BalanceInfo.objects.get_or_create(user = self.u2, userTo = self.u1, group = reciept.group)
        u3u1, _ = BalanceInfo.objects.get_or_create(user = self.u3, userTo = self.u1, group = reciept.group)
        
        items[1].delete()

        self.assertEqual(RecieptInfo.objects.get(user = self.u2, reciept = reciept).cost, 3)
        self.assertEqual(RecieptInfo.objects.get(user = self.u3, reciept = reciept).cost, 2*5)

        self.assertEqual(u2u1.amount, 3 )
        self.assertEqual(u3u1.amount, 2*5)

    def test_balance_with_transaction(self):
        self.test_balance_change_after_itemInfo_change()
        reciept = Reciept.objects.get(owner = self.u1)
        items = reciept.item_set.all()

        u2u1, _ = BalanceInfo.objects.get_or_create(user = self.u2, userTo = self.u1, group = reciept.group)
        u3u1, _ = BalanceInfo.objects.get_or_create(user = self.u3, userTo = self.u1, group = reciept.group)
    
        Transaction.objects.create(group = reciept.group, sender = self.u2, recipiant = self.u1, amount=3)

        self.assertEqual(u2u1.amount, 0)
        self.assertEqual(u3u1.amount, 2*5)