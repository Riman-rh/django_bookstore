from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "address", "phone")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields