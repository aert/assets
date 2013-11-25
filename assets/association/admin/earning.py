from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget
from suit.widgets import AutosizedTextarea
from django_select2 import AutoModelSelect2Field, Select2Widget
from import_export.admin import ExportMixin

from ..models import Student
from ..models import Earning

from ._common_ import EXPORT_FORMATS
from .invoice import InvoiceInline


###############################################################################
# Earnings
###############################################################################

class StudentChoice(AutoModelSelect2Field):
    queryset = Student.objects
    search_fields = ['name__icontains', 'surname__icontains']


class EarningForm(ModelForm):
    from_student_verbose_name = _('from student')
    from_student = StudentChoice(
        label=from_student_verbose_name.capitalize(),
        required=False,
        widget=Select2Widget(
            select2_options={
                'width': '220px',
                'placeholder': 'Lookup %s ...' % from_student_verbose_name
            }
        )
    )

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
        'label', 'description', 'from_other',
    )
    list_display = (
        'payment_date', 'earning_type', 'label', 'amount', 'payment_type',
        'is_internal', 'has_invoice',
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
                ('from_student', 'from_other'),
            ]
        }),
    ]


admin.site.register(Earning, EarningAdmin)
