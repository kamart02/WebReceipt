from genericpath import exists
from typing import get_origin
from xml.dom import ValidationErr
from django.forms import ValidationError
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Reciept, Item, ItemInfo, Transaction
from .forms import GroupForm, ItemFormSet, ManageForm, ManageFormSet, SignupForm, TransactionForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import  PermissionDenied
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.models import User
from .temporaryModels import BalanceInfo, RecieptInfo


def index(request):
    if request.user.is_authenticated:
        return redirect('groupView')
    else:
        return render(request, 'reciept/index.html')

@login_required(redirect_field_name='next', login_url='/accounts/login')
def recieptList(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    reciepts = Reciept.objects.filter(group = group).order_by('-date', '-time')

    accounts = group.accounts.exclude(id = request.user.id)
    amounts = []
    recieptAmounts = []

    for account in accounts:
        balinfo = BalanceInfo(user = request.user, group = group, userTo = account)
        amounts.append(balinfo.amount())


    context = {
        'reciepts': reciepts,
        'group_id': group_id,
        'accounts': zip(accounts, amounts),
    }
    return render(request, 'reciept/recieptList.html', context)

@login_required(redirect_field_name='next', login_url='/accounts/login')
def groupView(request):
    groups = Group.objects.filter(accounts__username = request.user.username)
    context = {
        'groups': groups,
    }
    return render(request, 'reciept/groupView.html', context)

@login_required(redirect_field_name='next', login_url='/accounts/login')
def recieptView(request, reciept_id, group_id):
    reciept = get_object_or_404(Reciept, id = reciept_id)
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    itemList = Item.objects.filter(reciept = reciept)

    recieptinfo = RecieptInfo(user = request.user, reciept = reciept)

    context = {
        'items': itemList,
        'reciept': reciept,
        'group_id': group_id,
        'wholeBoughtCost': recieptinfo.cost()
    }

    return render(request, 'reciept/recieptView.html', context)

@login_required(redirect_field_name='next', login_url='/accounts/login')
def recieptEdit(request, reciept_id, group_id):
    group = get_object_or_404(Group, id = group_id)
    reciept = get_object_or_404(Reciept, id = reciept_id)
    if not reciept.owner == request.user:
        raise PermissionDenied
    formset = ItemFormSet(request.POST or None, instance = reciept)

    if request.method == 'POST':
        if formset.is_valid():
            formset.instance = reciept
            formset.save()
            
            return redirect('reciept-list', group_id=group_id)

    context = {
        'formset' : formset,
        'reciept' : reciept,
        'group_id': group_id
    }
    
    return render(request, 'reciept/recieptEdit.html', context)

@login_required(redirect_field_name='next', login_url='/accounts/login')
def recieptManage(request, reciept_id , group_id):
    group = get_object_or_404(Group, id = group_id)
    reciept = get_object_or_404(Reciept, id = reciept_id)
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
                    if form.cleaned_data['purchasedAmount'] > 0:
                        itemInfo = itemList.get(id = form.cleaned_data['itemId']).iteminfo_set.get(user=request.user)
                        itemInfo.amount = form.cleaned_data['purchasedAmount']
                        itemInfo.save()
            return redirect('reciept-list', group_id=group_id)
        

    formset = ManageFormSet(request.POST or None, initial = initial)

    itemList = zip(itemList, formset)

    context = {
        'items': itemList,
        'reciept': reciept,
        'group_id': group_id,
        'formset': formset,

    }
    return render(request, 'reciept/recieptManage.html', context)


@login_required(redirect_field_name='next', login_url='/accounts/login')
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


@login_required(redirect_field_name='next', login_url='/accounts/login')
def removeReciept(request, reciept_id, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    reciept = get_object_or_404(Reciept, id = reciept_id)
    reciept.delete()
    return redirect('index')

@login_required(redirect_field_name='next', login_url='/accounts/login')
def removeRecieptConfirmation(request, reciept_id, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    reciept = get_object_or_404(Reciept, id = reciept_id)
    context = {
        'id': id,
        'date': reciept.date,
        'time': reciept.time,
        'group_id': group_id
    }
    return render(request, 'reciept/removalConfirmation.html', context)

@login_required(redirect_field_name='next', login_url='/accounts/login')
def addReciept(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied
    
    reciept = Reciept(group = group, owner = request.user)
    reciept.save()

    return redirect('reciept-edit', reciept_id = reciept.id, group_id = group_id)

@login_required(redirect_field_name='next', login_url='/accounts/login')
def transactionView(request, group_id):
    group = get_object_or_404(Group, id = group_id)
    if not group.accounts.filter(username = request.user.username).exists():
        raise PermissionDenied

    transactions = group.transaction_set.filter(Q(sender = request.user) | Q(recipiant = request.user)).order_by('-date','-time')

    form = TransactionForm(queryset = group.accounts.all().exclude(id = request.user.id), data = request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            if form.cleaned_data['amount'] > 0:
                newTransaction = Transaction(
                    amount = form.cleaned_data['amount'],
                    recipiant =  form.cleaned_data['recipiant'],
                    sender = request.user,
                    group = group
                )
                newTransaction.save()

                return redirect('transaction-view', group_id=group_id)

    context = {
        'transactions': transactions,
        'group_id': group_id,
        'user': request.user,
        'form': form
    }

    return render(request, 'reciept/transactionView.html', context)


def loginView(request):
    loginForm = LoginForm(data = request.POST or None)

    if request.method == 'POST':
        if loginForm.is_valid():
            userObj = authenticate(request, username = loginForm.cleaned_data['username'], password = loginForm.cleaned_data['password'])
            if userObj != None:
                login(request, userObj)
                return redirect('index')
            else:
                loginForm.add_error(None, 'Invalid username or password')


    context = {
        'form': loginForm,
        'next': request.GET.get('next') or ''
    }

    return render(request, 'registration/login.html', context)

def logoutMethod(request):
    logout(request)

    return redirect('login')

def signupView(request):
    signupForm = SignupForm(data = request.POST or None)

    if request.method == 'POST':
        if signupForm.is_valid():
            if not User.objects.filter(username=signupForm.cleaned_data['username']).exists():
                try:
                    password_validation.validate_password(signupForm.cleaned_data['password1'])
                    if signupForm.cleaned_data['password1'] == signupForm.cleaned_data['password2']:
                        userObj = User.objects.create_user(signupForm.cleaned_data['username'], signupForm.cleaned_data['email'], signupForm.cleaned_data['password1'])
                        userObj.first_name = signupForm.cleaned_data['firstName']
                        userObj.last_name = signupForm.cleaned_data['lastName']
                        userObj.save()
                        login(request, userObj)
                        return redirect('index')
                    else:
                        signupForm.add_error(field='password2', error = 'Passwords not matching')
                except ValidationError:
                        signupForm.add_error(field='password1', error='Insufficient password')
            else:
                signupForm.add_error(field='username', error = 'Username already exists')

    context = {
        'form': signupForm
    }

    return render(request, 'registration/signup.html', context)