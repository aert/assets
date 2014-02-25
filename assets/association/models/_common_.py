from django.utils.translation import ugettext_lazy as _

APP_LABEL = 'association'

CHOICES_PAYMENT_TYPE = (
    (1, _('Cash')),
    (2, _('Credit Card')),
    (3, _('Bank Transfer')),
    (4, _('Bank Transfer - Auto')),
    (5, _('Cheque')),
)
