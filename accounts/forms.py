from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
User = get_user_model()


class SignUpForm(UserCreationForm):
    captcha = ReCaptchaField(label="", widget=ReCaptchaV2Checkbox, required = True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
