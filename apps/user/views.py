from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic
from library import settings
from apps.user.forms import SignUpForm, StripeForm
from apps.user.models import Tokens, Profile

def signup(request):
    """
    Sign up view. After filling the signup form,
    user is redirected to the payment page
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            login(request, user)
            request.session['username'] = username
            request.session['password'] = raw_password
            return render(request, 'user/prompt_payment.html')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


class StripeMixin(object):
    def get_context_data(self, **kwargs):
        context = super(StripeMixin, self).get_context_data(**kwargs)
        context['publishable_key'] = settings.STRIPE_PUBLIC_KEY
        return context


class ChargeView(StripeMixin, generic.FormView):
    """
    Completes the payment for registration
    """
    template_name = 'user/payment.html'
    form_class = StripeForm
    model = Tokens

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if (form.is_valid()):
            username = request.session['username']
            q1 = User.objects.get(username=username)
            q = Profile.objects.get(user_id=q1.id)
            q.payed = True
            q.save()
            return render(request, 'user/payment_success.html')
        return render(request, self.template_name, {'form': form})