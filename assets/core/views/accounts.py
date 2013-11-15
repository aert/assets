from django.views.generic.base import TemplateView


class AccountDetailView(TemplateView):
    template_name = 'accounts_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        return context


class AccountLogoutView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(AccountLogoutView, self).get_context_data(**kwargs)
        return context


class AccountLoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(AccountLoginView, self).get_context_data(**kwargs)
        return context
