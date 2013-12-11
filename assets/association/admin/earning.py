from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget
from suit.widgets import AutosizedTextarea
from import_export.admin import ExportMixin

from ..models import Earning
from ..models import EarningType

from ._common_ import EXPORT_FORMATS
from .invoice import InvoiceInline


###############################################################################
# Earning Types
###############################################################################

class EarningTypeAdmin(ModelAdmin):
    search_fields = (
        'label',
    )
    list_display = ('label', 'is_internal',)
    list_filter = ('is_internal',)

    fieldsets = [
        (None, {'fields': ['label', 'is_internal']}),
    ]


###############################################################################
# Earnings
###############################################################################

class EarningForm(ModelForm):
    class Meta:
        model = Earning
        widgets = {
            'payment_date': SuitDateWidget,
            'amount': TextInput(attrs={'class': 'input-small'}),
            'description': AutosizedTextarea,
        }


class EarningAdmin(ExportMixin, ModelAdmin):
    form = EarningForm
    inlines = [InvoiceInline]
    formats = EXPORT_FORMATS
    search_fields = (
        'label', 'description',
    )
    list_display = (
        'payment_date', 'earning_type', 'label', 'amount', 'payment_type',
        'invoices_link',
    )
    list_filter = (
        'payment_date', 'earning_type', 'has_invoice',
    )
    date_hierarchy = 'payment_date'

    fieldsets = [
        (None, {
            'fields': [
                'payment_date',
                ('earning_type', 'payment_type'),
                'label', 'amount',
                'description',
            ]
        }),
    ]

    def invoices_link(self, obj):
        if not obj.has_invoice:
            return ""
        url = reverse('admin:association_invoice_changelist')
        querystring = 'q=&earning__id__exact={}'.format(obj.pk)
        return u"<a href='{}?{}'>{}</a>".format(
            url, querystring, _('Display'))
    invoices_link.admin_order_field = 'has_invoice'
    invoices_link.allow_tags = True
    invoices_link.short_description = _('invoice')


admin.site.register(EarningType, EarningTypeAdmin)
admin.site.register(Earning, EarningAdmin)
