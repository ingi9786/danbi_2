from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/'
