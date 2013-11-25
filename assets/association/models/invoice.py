from __future__ import unicode_literals
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify

from ._common_ import CHOICES_PAYMENT_TYPE, APP_LABEL
from .earning import Earning
from .spending import Spending


###############################################################################
# INVOICE
###############################################################################

fs = FileSystemStorage(location=settings.PROTECTED_MEDIA_ROOT,
                       base_url=settings.PROTECTED_MEDIA_URL)


@python_2_unicode_compatible
class Invoice(models.Model):
    INVOICE_UNKNOWN = 0
    INVOICE_EARNING = 1
    INVOICE_SPENDING = 2
    CHOICES_INVOICE_TYPE = (
        (INVOICE_UNKNOWN, _('Unrecorded')),
        (INVOICE_EARNING, _('Earning')),
        (INVOICE_SPENDING, _('Spending')),
    )

    # Payment infos
    invoice_date = models.DateTimeField(_('invoice date'))

    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    label = models.CharField(_('label'), max_length=250)
    payment_type = models.PositiveSmallIntegerField(
        _('payment type'), choices=CHOICES_PAYMENT_TYPE)

    # Invoice Infos
    invoice_type = models.PositiveSmallIntegerField(
        _('type'), choices=CHOICES_INVOICE_TYPE, editable=False)
    earning = models.ForeignKey(Earning, null=True, blank=True)
    spending = models.ForeignKey(Spending, null=True, blank=True)

    buyer = models.CharField(_('buyer'), max_length=250, blank=True)
    seller = models.CharField(_('seller'), max_length=250, blank=True)

    def upload_path(self, filename):
        filename, ext = os.path.splitext(filename)
        return 'invoices/%s-%s%s' % (
            self.invoice_date.strftime("%Y%m"),
            slugify(filename),
            ext.lower())

    document = models.FileField(
        _('document'), max_length=250, blank=True, null=True,
        upload_to=upload_path, storage=fs)

    # Generic date infos
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-invoice_date']
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        app_label = APP_LABEL

    def __str__(self):
        return smart_text(
            '{}: {}'.format(self.invoice_date.strftime("%Y-%m-%d"),
                            self.label))

    def save(self, *args, **kwargs):
        # invoice_type
        if self.earning_id and not self.spending_id:
            self.invoice_type = self.INVOICE_EARNING
        elif not self.earning_id and self.spending_id:
            self.invoice_type = self.INVOICE_SPENDING
        else:
            self.invoice_type = self.INVOICE_UNKNOWN

        # compute foreign keys
        if self.earning_id:
            self.earning.has_invoice = True
            self.earning.save()
        if self.spending_id:
            self.spending.has_invoice = True
            self.spending.save()

        super(Invoice, self).save(*args, **kwargs)

    def delete(self):
        # compute foreign keys
        if self.earning_id:
            count = Invoice.objects.filter(earning=self.earning).count()
            self.earning.has_invoice = count > 1
            self.earning.save()
        if self.spending_id:
            count = Invoice.objects.filter(spending=self.spending).count()
            self.spending.has_invoice = count > 1
            self.spending.save()

        super(Invoice, self).delete()

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.earning_id and self.spending_id:
            raise ValidationError(
                _('Invoice must be either an Earning or a Spending.'))

    def get_document_link(self):
        if self.document:
            return "<a href='%s' target='_blank'>%s</a>" % (
                self.document.url, _('Download'))
        else:
            return ""
    get_document_link.admin_order_field = 'document'
    get_document_link.allow_tags = True
    get_document_link.short_description = _('document')

    def has_document(self):
        return not not self.document
    has_document.admin_order_field = 'document'
    has_document.boolean = True
    has_document.short_description = _('document ?')
