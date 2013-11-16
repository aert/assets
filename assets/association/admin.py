from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget, AutosizedTextarea
from .models import Student
from .models import Treasury


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
admin.site.register(Treasury)
