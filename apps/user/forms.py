from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from apps.user.models import Tokens

class SignUpForm(UserCreationForm):
    """
        User signup form
    """
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class StripeForm(forms.Form):
    """
        Registration payment form
    """
    number = forms.IntegerField(required=True, label="Card Number", initial=4242424242424242)
    exp_month = forms.IntegerField(initial=12)
    exp_year = forms.IntegerField(initial=2019,required=True)
    cvv = forms.IntegerField(required=True, label="CVV Number", max_value=999, widget=forms.TextInput(attrs={'size': '3'}))
    stripe_token = forms.CharField()

    def clean(self):
        cleaned = super(StripeForm, self).clean()
        if not self.errors:
            number = self.cleaned_data["number"]
            exp_month = self.cleaned_data["exp_month"]
            exp_year = self.cleaned_data["exp_year"]
            cvv = self.cleaned_data["cvv"]
            token = self.cleaned_data["stripe_token"]
            # import pdb
            # pdb.set_trace()
            print(token)
            tokenobj = Tokens()

            success, instance = tokenobj.charge(50, number, exp_month, exp_year, cvv, token)

            if not success:
                raise forms.ValidationError("Error: %s" % instance.get('message'))
            else:
                instance.save()
                pass

        return cleaned