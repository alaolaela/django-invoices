#coding: utf-8
from __future__ import absolute_import

import StringIO
from os import fdopen, remove
from tempfile import mkstemp
from zipfile import ZipFile, ZIP_DEFLATED

from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from django.http import Http404, HttpResponse
from django.utils.encoding import smart_str
from django.core.servers.basehttp import FileWrapper

from invoices import settings
from seautils.views.decorators import render_with, json_response, render_with_formats
from apps.documents.views import PDF_DOCUMENT_CONFIG, PDF_PREVIEW_DOCUMENT_CONFIG,\
        renderer_document_pdf

from ..invoices.forms import InvoiceItemFormset, INVOICE_TYPES_FORMS
from ..invoices.models import InvoiceItem, Invoice

STATUS_OK = 'ok'
STATUS_ERROR = 'error'
STATUS_KEY = 'status'

@render_with('office/index.html')
def index(request):
    return {}

@render_with('office/invoice_form.html')
def render_form(request, invoice_type):
    invoice_type = int(invoice_type)
    invoice_form = INVOICE_TYPES_FORMS[invoice_type]()
    invoice_item_formset = InvoiceItemFormset()
    return {'inv_f': invoice_form, 'inv_formset': invoice_item_formset}

@json_response
def save_form(request, invoice_type, invoice_id=None):
    if not request.method == 'POST':
        raise Http404
    invoice_type = int(invoice_type)
    resp_dat = {}
    dat = request.POST
    if invoice_id:
        pass
    else:
        invoice_form = INVOICE_TYPES_FORMS[invoice_type](dat)
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
        new_invoice.status = new_invoice.DEFAULT_STATUS
        new_invoice.save()
        
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


def renderer_documents_zipped(request, view_output, **kwargs):
    view_output.update({'document': request.document})
    files = []
    for invoice in view_output.get('invoices', []):
        view_output['invoice'] = invoice
        invoice_resp = renderer_document_pdf(request, view_output, **kwargs)
        fd, tmppath = mkstemp(suffix='.pdf')
        with fdopen(fd, 'wt') as f:
            f.write(smart_str(invoice_resp))
        files.append((tmppath, '%s.pdf' % invoice.key))

    buff= StringIO.StringIO()
    with ZipFile(buff, 'w') as invzip:
        [invzip.write(f[0], f[1]) for f in files]
    [remove(f[0]) for f in files]
    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename=faktury.zip'
    buff.seek(0)
    response.write(buff.read())
    return response

ZIPPED_DOCUMENTS_CONFIG = PDF_PREVIEW_DOCUMENT_CONFIG.copy()
ZIPPED_DOCUMENTS_CONFIG['renderer'] = renderer_documents_zipped

@render_with_formats(pdf=PDF_DOCUMENT_CONFIG, zip=ZIPPED_DOCUMENTS_CONFIG)
def invoice_print(request, *args, **kwargs):
    ids = request.GET.getlist('id')
    if len(ids) > 1:
        invoices = Invoice.objects.filter(id__in=ids)
        return {'invoices': invoices}
    
    invoice = Invoice.objects.get(id=ids[0])
    return {
        #'headers': {'Content-Disposition': 'attachment; filename=%s.pdf' % invoice.key},
        'invoice': invoice,
    }
