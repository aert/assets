from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget
from suit.widgets import AutosizedTextarea
from import_export.admin import ExportMixin

from ..models import Student

from ._common_ import EXPORT_FORMATS


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
