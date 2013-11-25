from __future__ import unicode_literals
import datetime
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify


###############################################################################
# STUDENTS
###############################################################################

@python_2_unicode_compatible
class Student(models.Model):
    CHOICES_LEVEL = (
        (0, _('Beginner')),
        (1, _('Elementary')),
        (2, _('Intermediate')),
    )

    name = models.CharField(_('name'), max_length=100)
    surname = models.CharField(_('surname'), max_length=100)
    adress = models.TextField(_('address'), blank=True)
    classroom = models.CharField(_('class'), blank=True, max_length=50)
    level = models.IntegerField(_('level'), choices=CHOICES_LEVEL, blank=True)
    phone = models.CharField(_('phone'), blank=True, max_length=60)
    parent = models.CharField(_('parent'), blank=True, max_length=200)
    email = models.EmailField(_('e-mail'), blank=True)

    is_active = models.BooleanField(_('is active'), default=True)
    last_registration = models.DateField(
        _('last registration'), default=datetime.datetime.now,
        blank=True, null=True
    )

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'surname']
        verbose_name = _('student')
        verbose_name_plural = _('students')

    def __str__(self):
        return smart_text('{} {}'.format(self.name, self.surname))


###############################################################################
# EARNING
###############################################################################

CHOICES_PAYMENT_TYPE = (
    (1, _('Cash')),
    (2, _('Credit Card')),
    (3, _('Bank Transfer')),
    (3, _('Bank Transfer - Auto')),
    (4, _('Cheque')),
)


@python_2_unicode_compatible
class Earning(models.Model):
    CHOICES_EARNING_TYPE = (
        (1, _('subscription (internal)')),
        (2, _('other (internal)')),
        (10, _('external')),
    )

    payment_date = models.DateField(
        _('payment date'), default=datetime.datetime.now)
    earning_type = models.PositiveSmallIntegerField(
        _('earning type'), choices=CHOICES_EARNING_TYPE)
    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    label = models.CharField(_('label'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    payment_type = models.PositiveSmallIntegerField(
        _('payment type'), choices=CHOICES_PAYMENT_TYPE)

    from_student = models.ForeignKey(Student, verbose_name=_('from student'),
                                     null=True, blank=True)
    from_other = models.CharField(_('from other'), max_length=250, blank=True)

    has_invoice = models.BooleanField(_('has invoice ?'), default=False,
                                      editable=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('earning')
        verbose_name_plural = _('earnings')

    def __str__(self):
        return smart_text('{}: {}'.format(self.payment_date, self.label))

    def is_internal(self):
        return self.earning_type != 10
    is_internal.admin_order_field = 'earning_type'
    is_internal.boolean = True
    is_internal.short_description = _('internal ?')


###############################################################################
# SPENDING
###############################################################################

@python_2_unicode_compatible
class Spending(models.Model):
    CHOICES_SPENDING_TYPE = (
        (1, _('fixed expenses')),
        (2, _('other')),
    )

    payment_date = models.DateField(
        _('payment date'), default=datetime.datetime.now)
    spending_type = models.PositiveSmallIntegerField(
        _('spending type'), choices=CHOICES_SPENDING_TYPE)
    amount = models.DecimalField(_('amount'), max_digits=15, decimal_places=2)
    label = models.CharField(_('label'), max_length=250)
    description = models.TextField(_('description'), blank=True)
    payment_type = models.PositiveSmallIntegerField(
        _('payment type'), choices=CHOICES_PAYMENT_TYPE)

    to = models.CharField(_('to'), max_length=250, blank=True)

    has_invoice = models.BooleanField(_('has invoice ?'), default=False,
                                      editable=False)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('spending')
        verbose_name_plural = _('spendings')

    def __str__(self):
        return smart_text('{}: {}'.format(self.payment_date, self.label))


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
