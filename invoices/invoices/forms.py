#coding: utf-8

from __future__ import absolute_import

from django import forms
from django.forms.models import inlineformset_factory 
from django.contrib.contenttypes.models import ContentType

from .models import Invoice, InvoiceItem
from .. import settings

class InvoiceForm(forms.models.ModelForm):
    ct_ids = [ContentType.objects.get_by_natural_key(*m.lower().split('.')).id\
                for m in settings.CUSTOMER_MODELS]
    class Meta:
        model = Invoice
        widgets = {
            'sale_type': forms.RadioSelect(),
            'customer_object_id': forms.Select(choices=()),
        }
    customer_content_type = forms.ModelChoiceField(queryset=ContentType.\
                objects.filter(id__in=ct_ids))

class InvoiceItemForm(forms.models.ModelForm):
    class Meta:
        model = InvoiceItem

InvoiceItemFormset = inlineformset_factory(Invoice, InvoiceItem, extra=1)
