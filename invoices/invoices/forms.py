#coding: utf-8

from __future__ import absolute_import

from django import forms
from django.forms.models import inlineformset_factory 
from django.contrib.contenttypes.models import ContentType

from .models import Invoice, InvoiceItem, VatInvoice, ProformaInvoice, INVOICE_TYPE_VAT,\
        INVOICE_TYPE_PROFORMA
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
        exclude = ('status',)
    customer_content_type = forms.ModelChoiceField(queryset=ContentType.\
                objects.filter(id__in=ct_ids))

class VatInvoiceForm(InvoiceForm):
    class Meta(InvoiceForm.Meta):
        model = VatInvoice

class ProformaInvoiceForm(InvoiceForm):
    class Meta(InvoiceForm.Meta):
        model = ProformaInvoice

INVOICE_TYPES_FORMS = {
    INVOICE_TYPE_VAT: VatInvoiceForm,
    INVOICE_TYPE_PROFORMA: ProformaInvoiceForm
}

class InvoiceItemForm(forms.models.ModelForm):
    class Meta:
        model = InvoiceItem
        widgets = {
            'product_object_id': forms.HiddenInput(),
            'product_content_type': forms.HiddenInput(),
        }

InvoiceItemFormset = inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=1,
        can_delete=1)
