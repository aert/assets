from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.encoding import smart_text


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


@python_2_unicode_compatible
class Treasury(models.Model):
    CHOICES_MONTH = (
        (1, _('January')),
        (2, _('February')),
        (3, _('March')),
        (4, _('April')),
        (5, _('May')),
        (6, _('June')),
        (7, _('July')),
        (8, _('August')),
        (9, _('September')),
        (10, _('October')),
        (11, _('November')),
        (12, _('December')),
    )

    month = models.IntegerField(_('month'), choices=CHOICES_MONTH)
    year = models.IntegerField(_('year'))

    is_deleted = models.BooleanField(_('is deleted'), default=False)

    class Meta:
        verbose_name = _('treasury')
        verbose_name_plural = _('treasury')

    def __str__(self):
        return smart_text('{}/{}'.format(self.month, self.year))
