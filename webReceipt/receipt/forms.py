from django import forms
from django.forms import BaseInlineFormSet, CheckboxInput, HiddenInput, ModelForm, fields, inlineformset_factory
from django.forms.formsets import formset_factory
from . import models



class ItemForm(ModelForm):
    class Meta:
        model = models.Item
        fields = [
            'name', 'amount', 'price'
        ]
    
    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

    

class ItemFormSetWithWidget(BaseInlineFormSet):
    def get_deletion_widget(self):
        return CheckboxInput(attrs={'class': 'form-check-input'})

ItemFormSet = inlineformset_factory(
    models.Receipt,
    models.Item,
    ItemForm,
    can_delete=True,
    extra=0,
    formset=ItemFormSetWithWidget
)

class GroupForm(ModelForm):
    class Meta:
        model = models.Group
        fields = [
            'name', 'accounts'
        ]   

class ManageForm(forms.Form):
    purchasedAmount = forms.DecimalField(decimal_places=2, max_digits=9)
    itemId = forms.IntegerField(widget=forms.HiddenInput)
    purchasedAmount.widget.attrs.update({
        'class': 'form-control mt-1',
        }
    )

ManageFormSet = formset_factory(
    ManageForm,
    can_delete=False,
    extra = 0,
)

class TransactionForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=9)
    recipiant = forms.ModelChoiceField(queryset=None)

    amount.widget.attrs.update({
        'class': 'form-control mt-0',
        }
    )
    recipiant.widget.attrs.update({
        'class': 'form-control mt-0',
        }
    )

    def __init__(self, queryset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipiant'].queryset = queryset

class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    username.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Username'
        }
    )
    password.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Password'
        }
    )

class SignupForm(forms.Form):
    username = forms.CharField(max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    firstName = forms.CharField(max_length=254)
    lastName = forms.CharField(max_length=254)
    email = forms.EmailField(max_length = 254)

    username.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Username'
        }
    )

    password1.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Password'
        }
    )

    password2.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Confirm password'
        }
    )

    firstName.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'First name'
        }
    )

    lastName.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Last name'
        }
    )

    email.widget.attrs.update({
        'class': 'form-control mt-1',
        'placeholder': 'Email'
        }
    )
    