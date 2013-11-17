from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget, AutosizedTextarea
from .models import Student
from .models import Earning
from .models import Spending


###############################################################################
# STUDENTS
###############################################################################

class StudentForm(ModelForm):
    class Meta:
        widgets = {
            'adress': AutosizedTextarea,
            'last_registration': SuitDateWidget,
        }


class StudentAdmin(ModelAdmin):
    form = StudentForm
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
            'fields': ['level', 'classroom', 'last_registration', 'is_active']}),
    ]


admin.site.register(Student, StudentAdmin)


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


class EarningAdmin(ModelAdmin):
    form = EarningForm
    search_fields = (
        'label', 'description', 'from_other',
    )
    list_display = (
        'payment_date', 'earning_type', 'label', 'amount', 'payment_type',
        'updated',
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


class SpendingAdmin(ModelAdmin):
    form = SpendingForm
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
