import datetime
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..facades import get_yearly_dashboard_data
#import logging


def view_dashboard(request):
    template_name = 'admin/dashboard/welcome.html'
    context = RequestContext(request)

    # Get results
    year = datetime.datetime.now().year
    results, total_earning, total_spending = get_yearly_dashboard_data(year)

    # Send to Template
    context['title'] = _('Dashboard')
    context['results'] = results
    context['total_earning'] = total_earning
    context['total_spending'] = total_spending


    return render_to_response(
        template_name, context_instance=context)
