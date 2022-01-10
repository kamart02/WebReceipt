from typing import get_origin
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Reciept, Item, ItemInfo, Transaction
from .forms import GroupForm, ItemFormSet, ManageForm, ManageFormSet, TransactionForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  PermissionDenied
from django.db.models import Q



# Create your views here.

from django.http import HttpResponse
import datetime

@login_required
def recieptList(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    reciepts = Reciept.objects.filter(group = group).order_by('-date', '-time')
    context = {
        'reciepts': reciepts,
        'group_id': group_id
    }
    return render(request, 'reciept/index.html', context)

@login_required
def groupView(request):
    groups = Group.objects.filter(accounts__username = request.user.username)
    context = {
        'groups': groups,
    }
    return render(request, 'reciept/group.html', context)

@login_required
def recieptView(request, id, group_id):
    reciept = get_object_or_404(Reciept, id=id)
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    itemList = Item.objects.filter(reciept = reciept)

    context = {
        'items': itemList,
        'reciept': reciept,
        'group_id': group_id
    }

    return render(request, 'reciept/recieptView.html', context)

@login_required
def recieptEdit(request, id, group_id):
    group = get_object_or_404(Group, id = group_id)
    reciept = get_object_or_404(Reciept, id=id)
    if not reciept.owner == request.user:
        raise PermissionDenied
    formset = ItemFormSet(request.POST or None, instance=reciept)

    if request.method == 'POST':
        if formset.is_valid():
            formset.instance = reciept
            formset.save()
            cost = 0
            itemList = Item.objects.filter(reciept=reciept)
            for item in itemList:
                item.cost = item.amount*item.price
                item.save()
                cost+=item.amount*item.price
            reciept.wholeCost = cost
            reciept.save()
            return redirect('reciept-view', id = id, group_id=group_id)

    context = {
        'formset' : formset,
        'reciept' : reciept,
        'group_id': group_id
    }
    
    return render(request, 'reciept/recieptEdit.html', context)

@login_required
def recieptManage(request, id , group_id):
    group = get_object_or_404(Group, id = group_id)
    reciept = get_object_or_404(Reciept, id=id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    itemList = Item.objects.filter(reciept = reciept)

    initial = []
    
    for item in itemList:
        info, _ = item.iteminfo_set.get_or_create(user = request.user, defaults = {
            'amount': 0,
            'user': request.user,
            'item': item
        })
        initial.append(
            {
                'itemId': item.id,
                'purchasedAmount': info.amount,
            }
        )

    if request.method == 'POST':
        formset = ManageFormSet(data = request.POST)
        
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data != {}:
                    # print(form.cleaned_data)
                    itemInfo = itemList.get(id = form.cleaned_data['itemId']).iteminfo_set.get(user=request.user)
                    itemInfo.amount = form.cleaned_data['purchasedAmount']
                    itemInfo.save()
            recieptInfo, _ = reciept.recieptinfo_set.get_or_create(user = request.user)
            recieptInfo.save()

        else:
            print(formset.errors)
        return redirect('reciept-view', id = id, group_id=group_id)

    formset = ManageFormSet(None, initial = initial)

    itemList = zip(itemList, formset)

    context = {
        'items': itemList,
        'reciept': reciept,
        'group_id': group_id,
        'formset': formset

    }
    return render(request, 'reciept/recieptManage.html', context)


@login_required
def addGroup(request):
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form': form.as_ul()
    }
    return render(request, 'reciept/groupNew.html', context)


@login_required
def removeReciept(request, id, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    reciept = get_object_or_404(Reciept, id=id)
    reciept.delete()
    return redirect('index')

@login_required
def removeRecieptConfirmation(request, id, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    reciept = get_object_or_404(Reciept, id=id)
    context = {
        'id': id,
        'date': reciept.date,
        'time': reciept.time,
        'group_id': group_id
    }
    return render(request, 'reciept/removalConfirmation.html', context)

@login_required
def addReciept(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    
    reciept = Reciept(wholeCost = 0, group = group, owner = request.user)
    reciept.save()

    return redirect('reciept-edit', id=reciept.id, group_id=group_id)

@login_required
def profile(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied

    groupUserProfile, _ = group.groupuserprofile_set.get_or_create(user = request.user)
    balancesInfo = groupUserProfile.balanceinfo_set.all()

    transactions = group.transaction_set.filter(Q(sender = request.user) | Q(recipiant = request.user))

    context = {
        'balances': balancesInfo,
        'transactions': transactions,
        'group_id': group_id,
        'user': request.user,
    }

    return render(request, 'reciept/profile.html', context)

@login_required
def newTransaction(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied

    accounts = group.accounts.all()

    if request.method == 'POST':
        form = TransactionForm(queryset=accounts, data = request.POST)
        if form.is_valid():
            newTransaction = Transaction(
                amount = form.cleaned_data['amount'],
                recipiant =  form.cleaned_data['recipiant'],
                sender = request.user,
                group = group
            )
            newTransaction.save()
            recipiantUserGroupProfile, _ = group.groupuserprofile_set.get_or_create(user = form.cleaned_data['recipiant'])
            userGroupProfile, _ = group.groupuserprofile_set.get_or_create(user = request.user)
            recipiantBalance, _ = recipiantUserGroupProfile.balanceinfo_set.get_or_create(userTo = request.user)
            userBalance, _ = userGroupProfile.balanceinfo_set.get_or_create(userTo = form.cleaned_data['recipiant'])

            recipiantBalance.amount += form.cleaned_data['amount']
            userBalance.amount -= form.cleaned_data['amount']
            recipiantBalance.save()
            userBalance.save()

            return redirect('profile', group_id=group_id)

    
    form = TransactionForm(queryset=accounts)

    context = {
        'form': form,
    }

    return render(request, 'reciept/newTransaction.html', context)