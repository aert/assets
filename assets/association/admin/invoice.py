from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin import StackedInline
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitSplitDateTimeWidget
from suit.widgets import AutosizedTextarea
from django_select2 import AutoModelSelect2Field, Select2Widget
from import_export.admin import ExportMixin

from ..models import Earning
from ..models import Spending
from ..models import Invoice

from ._common_ import EXPORT_FORMATS


class InvoiceInline(StackedInline):
    model = Invoice
    extra = 0
    widgets = {
        'invoice_date': SuitSplitDateTimeWidget,
        'amount': TextInput(attrs={'class': 'input-small'}),
    }
    fieldsets = [
        (None, {
            'fields': [
                ('invoice_date', 'payment_type'),
                ('label', 'amount'),
                ('buyer', 'seller'),
                'document']}),
    ]


###############################################################################
# Invoices
###############################################################################

class EarningChoice(AutoModelSelect2Field):
    queryset = Earning.objects
    search_fields = ['label__icontains', 'description__icontains']


class SpendingChoice(AutoModelSelect2Field):
    queryset = Spending.objects
    search_fields = ['label__icontains', 'description__icontains']


class InvoiceForm(ModelForm):
    earning = EarningChoice(
        label=_('Earning'),
        required=False,
        widget=Select2Widget(select2_options={'width': '220px'})
    )
    spending = SpendingChoice(
        label=_('Spending'),
        required=False,
        widget=Select2Widget(select2_options={'width': '220px'})
    )

    class Meta:
        model = Invoice
        widgets = {
            'invoice_date': SuitSplitDateTimeWidget,
            'amount': TextInput(attrs={'class': 'input-small'}),
            'description': AutosizedTextarea,
        }


class InvoiceAdmin(ExportMixin, ModelAdmin):
    form = InvoiceForm
    formats = EXPORT_FORMATS
    search_fields = (
        'label', 'description', 'buyer', 'seller',
    )
    list_display = (
        'invoice_date', 'invoice_type', 'label', 'amount', 'payment_type',
        'seller', 'get_document_link',
    )
    list_filter = ('invoice_date', 'invoice_type', 'payment_type',)
    date_hierarchy = 'invoice_date'

    fieldsets = [
        (_('Invoice'), {
            'fields': [
                'invoice_date', 'payment_type',
                'label', 'amount',
            ]
        }),
        (_('Details'), {
            'fields': [
                ('buyer', 'seller'),
                'document']}),
        (_('Link'), {
            'fields': [
                ('earning', 'spending')]}),
    ]

    #def has_add_permission(self, request):
    #    return False


admin.site.register(Invoice, InvoiceAdmin)
