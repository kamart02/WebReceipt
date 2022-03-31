import decimal

class BalanceInfo():
    
    def __init__(self, user, group, userTo):
        self.user = user
        self.group = group
        self.userTo = userTo

    def amount(self):
        receiptInfos = self.user.iteminfo_set.filter(item__receipt__group = self.group, item__receipt__owner = self.userTo)
        receiptInfosTo = self.userTo.iteminfo_set.filter(item__receipt__group = self.group, item__receipt__owner = self.user)
        
        amount = decimal.Decimal(0)

        for receiptInfo in receiptInfos:
            amount += receiptInfo.cost

        for receiptInfo in receiptInfosTo:
            amount -= receiptInfo.cost

        transactionsTo = self.user.sender.filter(group = self.group)
        transactionsFrom = self.user.recipiant.filter(group = self.group)

        for transaction in transactionsTo:
            amount -= transaction.amount

        for transaction in transactionsFrom:
            amount += transaction.amount

        return round(amount,2)

    def __str__(self):
        return "Group {}, {} to {}".format(self.groupUserProfile.group.name, self.groupUserProfile.user.username, self.userTo.username)


class receiptInfo():
    def __init__(self, user, receipt):
        self.user = user
        self.receipt = receipt
    #cost = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def cost(self):
        items = self.receipt.item_set.all()
        
        cost = decimal.Decimal(0)
        for item in items:
            itemInfo, _ = item.iteminfo_set.get_or_create(user = self.user)
            cost += itemInfo.cost

        return round(cost,2)