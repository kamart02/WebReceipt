from typing import get_origin
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Reciept, Item, ItemInfo
from .forms import GroupForm, ItemFormSet, ManageForm, ManageFormSet
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  PermissionDenied



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
                    print(form.cleaned_data)
                    info = itemList.get(id = form.cleaned_data['itemId']).iteminfo_set.get(user=request.user)
                    info.amount = form.cleaned_data['purchasedAmount']
                    info.save()
        else:
            print(formset.errors)
        return redirect('reciept-view', id = id, group_id=group_id)

    formset = ManageFormSet(None, initial = initial)
    print (formset)

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
    group = Group.objects.get(id = group_id)
    reciept = Reciept(wholeCost = 0, group = group, owner = request.user)
    reciept.save()

    return redirect('reciept-edit', id=reciept.id, group_id=group_id)