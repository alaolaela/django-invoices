#coding: utf-8

from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from django.http import Http404

from invoices import settings
from seautils.views.decorators import render_with, json_response

from ..invoices.forms import InvoiceItemFormset,InvoiceForm
from ..invoices.models import InvoiceItem

STATUS_OK = 'ok'
STATUS_ERROR = 'error'
STATUS_KEY = 'status'

@render_with('office/index.html')
def index(request):
    return {}

@render_with('office/invoice_form.html')
def render_form(request):
    invoice_form = InvoiceForm()
    invoice_item_formset = InvoiceItemFormset()
    return {'inv_f': invoice_form, 'inv_formset': invoice_item_formset}

@json_response
def save_form(request, invoice_id=None):
    if not request.method == 'POST':
        raise Http404
    resp_dat = {}
    dat = request.POST
    if invoice_id:
        pass
    else:
        invoice_form = InvoiceForm(dat)
        invoice_item_formset = InvoiceItemFormset(dat)


    errors = False
    if not invoice_form.is_valid():
        resp_dat['main_form_errors'] = dict(invoice_form.errors)
        errors = True
    if not invoice_item_formset.is_valid():
        resp_dat['items_form_errors'] = invoice_item_formset.errors
        errors = True

    if not errors:
        new_invoice = invoice_form.save()
        InvoiceItemFormset(dat, instance=new_invoice).save()
        resp_dat[STATUS_KEY] = STATUS_OK
    else:
        resp_dat[STATUS_KEY] = STATUS_ERROR

    
    return resp_dat

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
    
    items += [{'label': i, 'value': 1} for i in InvoiceItem.objects.\
            filter(name__icontains=request.GET['term']).values_list('name', flat=True)]

    return items
