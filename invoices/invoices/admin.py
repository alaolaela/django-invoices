#coding: utf-8
from __future__ import absolute_import

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

try:
    from genericadmin.admin import GenericAdminModelAdmin as ModelAdmin
except ImportError:
    from django.contrib.admin import ModelAdmin

from invoices import settings
from .models import Invoice, InvoiceItem


class InvoiceProductInlineAdmin(admin.StackedInline):
    model = InvoiceItem
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product_content_type":
            ids = [ContentType.objects.get_by_natural_key(*m.lower().split('.')).id\
                    for m in settings.PRODUCT_MODELS]
            kwargs["queryset"] = ContentType.objects.filter(id__in=ids)
        
        return super(InvoiceProductInlineAdmin, self)\
            .formfield_for_foreignkey(db_field, request, **kwargs)
   

class InvoiceAdmin(ModelAdmin):
    
    inlines = (InvoiceProductInlineAdmin,)
    
    def __init__(self, *args, **kwargs):
        super(InvoiceAdmin, self).__init__(*args, **kwargs)
        self.content_type_whitelist = []
        for model in settings.CUSTOMER_MODELS:
            self.content_type_whitelist.append(model.replace('.','/').lower())

admin.site.register(Invoice, InvoiceAdmin)
