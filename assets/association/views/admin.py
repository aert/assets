import datetime
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
#from ..models import Earning


CHOICES_YEAR = {}
for year in range(2012, datetime.datetime.now().year + 1):
    CHOICES_YEAR[year] = year
CHOICES_YEAR = (CHOICES_YEAR.items(),)
CHOICES_YEAR = ((2012, "2012"), (2013, "2013"),)


class DashboardForm(forms.Form):
    year = forms.ChoiceField(choices=CHOICES_YEAR)


def view_dashboard(request):
    template_name = 'admin/dashboard/welcome.html'
    context = RequestContext(request)

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
