from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin import StackedInline
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget
from suit.widgets import SuitSplitDateTimeWidget
from suit.widgets import AutosizedTextarea
from django_select2 import AutoModelSelect2Field, Select2Widget
from import_export.admin import ExportMixin
import import_export
from .models import Student
from .models import Earning
from .models import Spending
from .models import Invoice


EXPORT_FORMATS = (
    import_export.formats.base_formats.CSV,
    import_export.formats.base_formats.XLS,
    import_export.formats.base_formats.ODS,
)


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
# STUDENTS
###############################################################################

class StudentForm(ModelForm):
    class Meta:
        widgets = {
            'adress': AutosizedTextarea,
            'last_registration': SuitDateWidget,
        }


class StudentAdmin(ExportMixin, ModelAdmin):
    form = StudentForm
    formats = EXPORT_FORMATS
    search_fields = (
        'name', 'surname', 'classroom', 'email', 'parent',
    )
    list_display = (
        'name', 'surname', 'adress', 'classroom', 'level', 'phone',
        'parent', 'email', 'last_registration', 'is_active'
    )
    list_filter = ('level', 'classroom')
    date_hierarchy = 'last_registration'

    fieldsets = [
        (None, {
            'fields': ['name', 'surname', 'parent']
        }),
        (_('Contact'), {
            'fields': ['phone', 'email', 'adress']}),
        (_('Registration'), {
            'fields': ['level', 'classroom',
                       'last_registration', 'is_active']}),
    ]


admin.site.register(Student, StudentAdmin)


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
        'label', 'description', 'to',
    )
    list_display = (
        'payment_date', 'spending_type', 'label', 'amount', 'payment_type',
        'has_invoice',
    )
    list_filter = ('payment_date', 'spending_type', 'to',
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


###############################################################################
# Invoices
###############################################################################

class InvoiceForm(ModelForm):
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
        'buyer', 'seller', 'has_document',
    )
    list_filter = ('invoice_date', 'invoice_type', 'payment_type', 'seller')
    date_hierarchy = 'invoice_date'

    fieldsets = [
        (None, {
            'fields': [
                'invoice_date', 'payment_type',
                'label', 'amount',
            ]
        }),
        (_('Invoice'), {
            'fields': [
                ('buyer', 'seller'),
                'document']}),
    ]

    def has_add_permission(self, request):
        return False


admin.site.register(Invoice, InvoiceAdmin)
