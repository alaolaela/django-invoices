#coding: utf-8

from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model

from invoices import settings
from seautils.views.decorators import render_with, json_response

from ..invoices.forms import InvoiceItemFormset,InvoiceForm
from ..invoices.models import InvoiceItem


@render_with('office/index.html')
def index(request):
    a = InvoiceItemFormset(prefix="OKO")
    #print a.management_form
    print a.empty_form
    #for form in a:
    #    print form.as_table()
    
    return {}

@render_with('office/invoice_form.html')
def render_form(request):
    invoice_form = InvoiceForm()
    invoice_item_formset = InvoiceItemFormset()
    return {'inv_f': invoice_form, 'inv_formset': invoice_item_formset}

@json_response
def get_choices(request, ct_id):
    ct = ContentType.objects.get(id=ct_id)
    m_cls = ct.model_class()
    return [(unicode(m), m.id) for m in m_cls.objects.all()]

@json_response
def products_search(request):
    items = []
    for model in settings.PRODUCT_MODELS:
        model_cls = get_model(*model.split('.'))
        if hasattr(model_cls, 'get_for_autocomplete'):
            items += model_cls.get_for_autocomplete(request.GET['term'])
    
    items += list(InvoiceItem.objects.filter(name__icontains=request.GET['term']).values_list('name',
                    flat=True))

    return items
