from django.utils.translation import ugettext_lazy as _
from .models import Earning
from .models import Spending


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
    def __init__(self, month_num, amount_earning, amount_spending):
        self.month_num = month_num
        self.month_name = MONTHS[month_num]
        self.amount_earning = amount_earning
        self.amount_spending = amount_spending


def get_yearly_dashboard_data(year):
    total_earning = 0
    total_spending = 0

    results = []
    for month_num in range(1, 12):
        res = MonthlyResult(month_num, 0, 0)
        results.append(res)

    # Earnings
    amount_list = Earning.objects.filter(payment_date__year=year)
    if amount_list:
        for res in amount_list:
            month_num = res.payment_date.month
            results[month_num - 1].amount_earning += res.amount
            total_earning += res.amount

    # Spendings
    amount_list = Spending.objects.filter(payment_date__year=year)
    if amount_list:
        for res in amount_list:
            month_num = res.payment_date.month
            results[month_num - 1].amount_spending += res.amount
            total_spending += res.amount

    return (results, total_earning, total_spending)
