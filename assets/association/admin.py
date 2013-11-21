from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget, AutosizedTextarea
from django_select2 import AutoModelSelect2Field, Select2Widget
from import_export.admin import ExportMixin
import import_export
from .models import Student
from .models import Earning
from .models import Spending


EXPORT_FORMATS = (
    import_export.formats.base_formats.CSV,
    import_export.formats.base_formats.XLS,
    import_export.formats.base_formats.ODS,
)


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
        'name', 'surname', 'adress', 'classroom', 'email', 'parent',
        'last_registration'
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
    from_student_verbose_name = Earning._meta.\
        get_field_by_name('from_student')[0].verbose_name
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
    formats = EXPORT_FORMATS
    search_fields = (
        'label', 'description', 'from_other',
    )
    list_display = (
        'payment_date', 'earning_type', 'label', 'amount', 'payment_type',
        'updated', 'is_internal',
    )
    list_filter = (
        'payment_date', 'earning_type', 'payment_type',
        'from_student', 'from_other')
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
    formats = EXPORT_FORMATS
    search_fields = (
        'label', 'description', 'to',
    )
    list_display = (
        'payment_date', 'spending_type', 'label', 'amount', 'payment_type',
        'updated',
    )
    list_filter = ('payment_date', 'spending_type', 'payment_type', 'to')
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
