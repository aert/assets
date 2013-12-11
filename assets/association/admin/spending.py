from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget
from suit.widgets import AutosizedTextarea
from import_export.admin import ExportMixin

from ..models import Spending
from ..models import SpendingType

from ._common_ import EXPORT_FORMATS
from .invoice import InvoiceInline


###############################################################################
# Earning Types
###############################################################################

class SpendingTypeAdmin(ModelAdmin):
    search_fields = (
        'label',
    )
    list_display = ('label', 'is_recurrent',)
    list_filter = ('is_recurrent',)

    fieldsets = [
        (None, {'fields': ['label', 'is_recurrent']}),
    ]


###############################################################################
# Spendings
###############################################################################

class SpendingForm(ModelForm):
    class Meta:
        model = Spending
        widgets = {
            'payment_date': SuitDateWidget,
            'amount': TextInput(attrs={'class': 'input-small'}),
            'description': AutosizedTextarea,
        }


class SpendingAdmin(ExportMixin, ModelAdmin):
    form = SpendingForm
    inlines = [InvoiceInline]
    formats = EXPORT_FORMATS
    search_fields = (
        'label', 'description'
    )
    list_display = (
        'payment_date', 'spending_type', 'label', 'amount', 'payment_type',
        'invoices_link',
    )
    list_filter = ('payment_date', 'spending_type', 'has_invoice',)
    date_hierarchy = 'payment_date'

    fieldsets = [
        (None, {
            'fields': [
                'payment_date',
                'spending_type', 'payment_type',
                'label', 'amount', 'description',
            ]
        }),
    ]

    def invoices_link(self, obj):
        if not obj.has_invoice:
            return ""
        url = reverse('admin:association_invoice_changelist')
        querystring = 'q=&spending__id__exact={}'.format(obj.pk)
        return u"<a href='{}?{}'>{}</a>".format(
            url, querystring, _('Display'))
    invoices_link.admin_order_field = 'has_invoice'
    invoices_link.allow_tags = True
    invoices_link.short_description = _('invoice')


admin.site.register(SpendingType, SpendingTypeAdmin)
admin.site.register(Spending, SpendingAdmin)
