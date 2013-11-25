from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.forms import TextInput
from suit.widgets import SuitDateWidget
from suit.widgets import AutosizedTextarea
from import_export.admin import ExportMixin

from ..models import Spending

from ._common_ import EXPORT_FORMATS
from .invoice import InvoiceInline


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
        'label', 'description',
    )
    list_display = (
        'payment_date', 'spending_type', 'label', 'amount', 'payment_type',
        'has_invoice',
    )
    list_filter = ('payment_date', 'spending_type',
                   'has_invoice',)
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


admin.site.register(Spending, SpendingAdmin)
