from django.views.generic.base import TemplateView


class TreasuryView(TemplateView):
    template_name = 'treasury.html'

    def get_context_data(self, **kwargs):
        context = super(TreasuryView, self).get_context_data(**kwargs)
        return context
