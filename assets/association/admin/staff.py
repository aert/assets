from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from suit.widgets import SuitDateWidget
from suit.widgets import AutosizedTextarea
from import_export.admin import ExportMixin

from ..models import Staff

from ._common_ import EXPORT_FORMATS


###############################################################################
# STUDENTS
###############################################################################

class StaffForm(ModelForm):
    class Meta:
        widgets = {
            'adress': AutosizedTextarea,
            'description': AutosizedTextarea,
            'registration': SuitDateWidget,
        }


class StaffAdmin(ExportMixin, ModelAdmin):
    form = StaffForm
    formats = EXPORT_FORMATS
    search_fields = (
        'name', 'surname', 'description', 'adress', 'email', 'phone',
    )
    list_display = (
        'name', 'surname', 'availability', 'fees', 'description',
        'registration', 'is_active'
    )
    list_filter = ('availability',)
    date_hierarchy = 'registration'

    fieldsets = [
        (None, {
            'fields': [('name', 'surname'), 'description']
        }),
        (_('Contact'), {
            'fields': [('phone', 'email'), 'adress']}),
        (_('Availability'), {
            'fields': ['availability', 'fees',
                       'registration', 'is_active']}),
    ]


admin.site.register(Staff, StaffAdmin)
