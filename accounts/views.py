from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import LoginForm


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return reverse_lazy('dashboard:admin_dashboard')
        elif user.role == 'BIOMEDICAL_OFFICER':
            return reverse_lazy('dashboard:biomedical_dashboard')
        else:
            return reverse_lazy('dashboard:ward_staff_dashboard')


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')