from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VendedorRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
