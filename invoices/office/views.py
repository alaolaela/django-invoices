#coding: utf-8
from __future__ import absolute_import

import StringIO
from os import fdopen, remove
from tempfile import mkstemp
from zipfile import ZipFile

from django.contrib.contenttypes.models import ContentType
from django.db.models import get_model
from django.http import Http404, HttpResponse
from django.utils.encoding import smart_str
from django.db import connection


from invoices import settings
from seautils.views.decorators import render_with, json_response, render_with_formats
from apps.documents.views import PDF_DOCUMENT_CONFIG, PDF_PREVIEW_DOCUMENT_CONFIG,\
        renderer_document_pdf

from ..invoices.forms import InvoiceItemFormset, INVOICE_TYPES_FORMS
from ..invoices.models import InvoiceItem, Invoice, ProformaInvoice, INVOICE_TYPES

STATUS_OK = 'ok'
STATUS_ERROR = 'error'
STATUS_KEY = 'status'

@render_with('office/index.html')
def index(request):
    return {}

@render_with('office/invoice_form.html')
def render_form(request, invoice_type, invoice_id=None):
    invoice_type = int(invoice_type)
    if not invoice_id:
        invoice_form = INVOICE_TYPES_FORMS[invoice_type]()
        invoice_item_formset = InvoiceItemFormset()
    else:
        instance = INVOICE_TYPES[invoice_type].objects.get(id=invoice_id)
        invoice_form = INVOICE_TYPES_FORMS[invoice_type](instance=instance)
        invoice_item_formset = InvoiceItemFormset(instance=instance)

    return {'inv_f': invoice_form, 'inv_formset': invoice_item_formset}

@json_response
def save_form(request, invoice_type, invoice_id=None):
    if not request.method == 'POST':
        raise Http404
    invoice_type = int(invoice_type)
    resp_dat = {}
    dat = request.POST.copy()
    if invoice_id:
        instance = INVOICE_TYPES[invoice_type].objects.get(id=invoice_id)
        invoice_form = INVOICE_TYPES_FORMS[invoice_type](dat, instance=instance)
        invoice_item_formset = InvoiceItemFormset(dat, instance=instance)
    else:
        invoice_form = INVOICE_TYPES_FORMS[invoice_type](dat)
        invoice_item_formset = InvoiceItemFormset(dat)
    
    errors = False
    resp_dat['main_form_info'] = {}
    if 'key' in dat and not invoice_form._meta.model.validate_key(dat['key']):
        resp_dat['key'] = invoice_form._meta.model.generate_next_key()
        dat['key'] = resp_dat['key']
        resp_dat['main_form_info']['key'] = (u'Wygenerowano nowy numer faktury',)
        errors = True
    elif 'key' not in dat:
        resp_dat['key'] = invoice_form._meta.model.generate_next_key()
        dat['key'] = resp_dat['key']

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
def prof_into_vat(request, inv_id):
    inv = ProformaInvoice.objects.get(id=inv_id)
    inv_v = inv.clone_as_vat()
    return {'status': 'OK', 'key': inv_v.key}

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
    items += InvoiceItem.get_for_autocomplete(request.GET['term'])
    return items

@json_response
def invoice_additional_info(request, invoice_ids):
    """ gross_price and others
    """
    try:
        invoice_ids_int = [int(a) for a in invoice_ids.split(',')]
    except ValueError:
        raise Http404('Incorrect ids')
    cursor = connection.cursor()
    tab = InvoiceItem._meta.db_table
    res = cursor.execute("SELECT SUM((100 + %(tab)s.tax) * %(tab)s.net_price), invoice_id  from %(tab)s"\
            " WHERE invoice_id in (%(ids)s) GROUP BY invoice_id" % {'tab': tab,
                'ids': ','.join(map(str, invoice_ids_int))}).fetchall()
    
    info = {inv_id: {'gross_price': val / 100} for val, inv_id in res}
    for invoice in Invoice.objects.filter(id__in=invoice_ids_int):
        if not invoice.id in info:
            info[invoice.id] = {'gross_price': 0}
        key = info[invoice.id]
        key['get_currency_display'] = invoice.get_currency_display()
        key['customer_invoice_data'] = invoice.customer.get_invoice_data()
        key['get_payment_type_display'] = invoice.get_payment_type_display()
        key['get_status_display'] = invoice.get_status_display()
    
    return info

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
def render_invoice(request, format):
    ids = request.GET.getlist('id')
    invoices = Invoice.objects.filter(id__in=ids)
    if format == 'pdf':
        return {'invoice': invoices[0]}
    else:
        return {'invoices': invoices}
