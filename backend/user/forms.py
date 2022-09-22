from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from .password_validation import NumericSpecialCharValidator as V

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if V.validate(password1):
            return password1

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email',)