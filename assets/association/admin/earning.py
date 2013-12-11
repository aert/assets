from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.forms import TextInput
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
        'has_invoice',
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


admin.site.register(EarningType, EarningTypeAdmin)
admin.site.register(Earning, EarningAdmin)
