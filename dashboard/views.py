from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'backend/dashboard/home.html'



class ResetPasswordView(TemplateView):
    template_name = 'backend/reset-password.html'
    title = 'تغییر رمز عبور'
