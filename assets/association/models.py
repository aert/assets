from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text


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

    from_student = models.ForeignKey(Student, null=True, blank=True)
    from_other = models.CharField(_('from other'), max_length=250, blank=True)

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

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']
        verbose_name = _('spending')
        verbose_name_plural = _('spendings')

    def __str__(self):
        return smart_text('{}: {}'.format(self.payment_date, self.label))
