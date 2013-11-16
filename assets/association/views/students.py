from django.views.generic.base import TemplateView


class StudentsView(TemplateView):
    template_name = 'students.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsView, self).get_context_data(**kwargs)
        return context


class StudentsViewDetail(TemplateView):
    template_name = 'students_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudentsViewDetail, self).get_context_data(**kwargs)
        return context
