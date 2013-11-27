from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text

from ._common_ import APP_LABEL


###############################################################################
# StaffS
###############################################################################

@python_2_unicode_compatible
class Staff(models.Model):
    CHOICES_AVAILABILITY = (
        (0, _('Unknown')),
        (1, _('Part-Time')),
        (2, _('Full-Time')),
    )

    name = models.CharField(_('name'), max_length=100)
    surname = models.CharField(_('surname'), max_length=100)
    title = models.CharField(_('title'), blank=True, max_length=100)

    availability = models.IntegerField(_('availability'),
                                       choices=CHOICES_AVAILABILITY,
                                       blank=True, default=0)
    fees = models.DecimalField(_('fees'), max_digits=15, decimal_places=2,
                               null=True, blank=True)

    adress = models.TextField(_('address'), blank=True)
    phone = models.CharField(_('phone'), blank=True, max_length=60)
    email = models.EmailField(_('e-mail'), blank=True)
    description = models.TextField(_('description'), blank=True)

    is_active = models.BooleanField(_('is active'), default=True)
    registration = models.DateField(
        _('registration'), default=datetime.datetime.now,
        blank=True, null=True
    )

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', 'surname']
        verbose_name = _('Staff')
        verbose_name_plural = _('Staff')
        app_label = APP_LABEL

    def __str__(self):
        return smart_text('{} {}'.format(self.name, self.surname))

    def has_fee(self):
        return not not self.fees
    has_fee.admin_order_field = 'fees'
    has_fee.boolean = True
    has_fee.short_description = _('fee ?')
