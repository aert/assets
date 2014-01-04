import datetime
from django.utils.translation import ugettext_lazy as _
from ..models.earning import Earning
from ..models.earning import EarningType
from ..models.spending import Spending
from ..models.spending import SpendingType


MONTHS = {
    1:  _('January'),
    2:  _('February'),
    3:  _('March'),
    4:  _('April'),
    5:  _('May'),
    6:  _('June'),
    7:  _('July'),
    8:  _('August'),
    9:  _('September'),
    10: _('October'),
    11: _('November'),
    12: _('December'),
}


class MonthlyResult(object):
    def __init__(
            self, month_num, amount_earning, amount_spending,
            earning_type, spending_type, is_internal, is_recurrent):
        self.month_num = month_num
        self.month_name = MONTHS[month_num]
        self.amount_earning = amount_earning
        self.amount_spending = amount_spending

        self.earning_type = earning_type
        self.spending_type = spending_type
        self.is_internal = is_internal
        self.is_recurrent = is_recurrent


def get_yearly_dashboard_data(year):
    total_earning = 0
    total_spending = 0

    earning_types = EarningType.objects.all()
    spending_types = SpendingType.objects.all()

    # Init
    results_earnings = {}
    for e_type in earning_types:
        type_results = []
        for month_num in range(1, 13):
            res = MonthlyResult(
                month_num, 0, 0, e_type.label, "", e_type.is_internal, False)
            type_results.append(res)
        results_earnings[e_type.label] = type_results
    results_spendings = {}
    for s_type in spending_types:
        type_results = []
        for month_num in range(1, 13):
            res = MonthlyResult(
                month_num, 0, 0, "", s_type.label, False, s_type.is_recurrent)
            type_results.append(res)
        results_spendings[s_type.label] = type_results

    # Earnings
    amount_list = Earning.objects.filter(payment_date__year=year)
    if amount_list:
        for res in amount_list:
            month_num = res.payment_date.month
            m_earn = results_earnings[res.earning_type.label][month_num - 1]
            m_earn.amount_earning += res.amount
            total_earning += res.amount

    # Spendings
    amount_list = Spending.objects.filter(payment_date__year=year)
    if amount_list:
        for res in amount_list:
            month_num = res.payment_date.month
            m_spend = results_spendings[res.spending_type.label][month_num - 1]
            m_spend.amount_spending += res.amount
            total_spending += res.amount

    return (results_earnings, results_spendings, total_earning, total_spending)


def get_years(since_year=2013):
    """ Return the list of selectable years for the Dashboard. """
    current_year = datetime.datetime.now().year
    results = []

    for year in range(since_year, current_year + 1):
        results.append(year)

    return results
