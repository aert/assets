from rest_framework import viewsets

from ..models import Earning
from ..models import EarningType
from ..models import Spending
from ..models import SpendingType
from ..models import Student
from ..models import Staff
from ..models import Invoice


class EarningViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Earnings to be viewed or edited.
    """
    model = Earning


class EarningTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Earning Types to be viewed or edited.
    """
    model = EarningType


class SpendingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Spendings to be viewed or edited.
    """
    model = Spending


class SpendingTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Spending Types to be viewed or edited.
    """
    model = SpendingType


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Students to be viewed or edited.
    """
    model = Student


class StaffViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Staff to be viewed or edited.
    """
    model = Staff


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Invoices to be viewed or edited.
    """
    model = Invoice
