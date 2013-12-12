import datetime
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext
from ..facades.dashboard import MONTHS
from ..facades.dashboard import get_yearly_dashboard_data
#import logging


def index(request):
    template_name = 'admin/dashboard/welcome.html'
    context = RequestContext(request)

    # Get results
    year = datetime.datetime.now().year
    results_earnings, results_spendings, total_earning, total_spending, = \
        get_yearly_dashboard_data(year)

    # Hide 0 values
    ignored_month = []
    for m in range(0, 12):
        ignored = True
        for r in results_earnings.values():
            if r[m].amount_earning != 0:
                ignored = False
        for r in results_spendings.values():
            if r[m].amount_spending != 0:
                ignored = False
        if ignored:
            ignored_month.append(m+1)

    month_name = MONTHS.copy()
    if len(ignored_month) > 0:
        filtered_earnings = results_earnings
        filtered_spendings = results_spendings
        for m in ignored_month:
            del month_name[m]
            for etype, month_values in results_earnings.items():
                filtered_earnings[etype] = [m_val for m_val in month_values if m_val.month_num != m]
            for stype, month_values in results_spendings.items():
                filtered_spendings[stype] = [m_val for m_val in month_values if m_val.month_num != m]
        results_earnings = filtered_earnings
        results_spendings = filtered_spendings

    # Send to Template
    context['title'] = _('Dashboard')
    context['results_earnings'] = results_earnings
    context['results_spendings'] = results_spendings
    context['total_earning'] = total_earning
    context['total_spending'] = total_spending
    context['month_names'] = month_name.values()

    return render_to_response(
        template_name, context_instance=context)
