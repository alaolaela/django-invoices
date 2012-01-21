#coding: utf-8
from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class InvoiceBase(models.Model):

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    customer = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True

    def get_document_number(self):
        raise NotImplementedError
