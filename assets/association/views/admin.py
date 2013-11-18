import datetime
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
#from ..models import Earning


CHOICES_YEAR = {}
for year in range(2012, datetime.datetime.now().year + 1):
    CHOICES_YEAR[year] = "{}".format(year)
CHOICES_YEAR = CHOICES_YEAR.items()


class DashboardForm(forms.Form):
    year = forms.ChoiceField(
        choices=CHOICES_YEAR, label='',
        initial=datetime.datetime.now().year)
    year.widget.attrs['class'] = 'auto-width search-filter'


def view_dashboard(request):
    template_name = 'admin/dashboard/welcome.html'
    context = RequestContext(request)

    context['title'] = _('Dashboard')

    if request.method == 'POST':
        form = DashboardForm()
        if form.is_valid():
            results = form.save()
            return render_to_response(
                template_name, {'form': form, 'results': results},
                context_instance=context)
    else:
        form = DashboardForm()
    return render_to_response(
        template_name, {'form': form}, context_instance=context)
