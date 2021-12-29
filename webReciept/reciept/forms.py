from django import forms
from django.forms import ModelForm, fields, inlineformset_factory
from django.forms.formsets import formset_factory
from . import models


class ItemForm(ModelForm):
    class Meta:
        model = models.Item
        fields = [
            'name', 'amount', 'price'
        ]

ItemFormSet = inlineformset_factory(
    models.Reciept,
    models.Item,
    ItemForm,
    can_delete=True,
    extra=2,
    exclude = ['payer']
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

ManageFormSet = formset_factory(
    ManageForm,
    can_delete=False,
    extra = 0,
)