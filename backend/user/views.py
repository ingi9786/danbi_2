from django.views.generic.edit import FormView, CreateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import User



class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/user/login'


class UserLoginView(FormView):
    model = User
    form_class =  CustomUserLoginForm
    template_name = 'login.html'
    success_url = '/routine/'
    
    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            logout(self.request)
            login(self.request, user)
        return HttpResponseRedirect(redirect_to=self.get_success_url())