from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in
from library import settings


class Profile(models.Model):
    """
       For users
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Tokens(models.Model):
    """
        Stripe token generator
    """
    charge_id = models.CharField(max_length=32,blank=True)

    def __init__(self, *args, **kwargs):
        super(Tokens, self).__init__(*args, **kwargs)

        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stripe = stripe

    def charge(self, price_in_cents, email ,number, exp_month, exp_year, cvc, token):
        if self.charge_id:
            return False, Exception(message="Already charged.")
        try:
            response = self.stripe.Charge.create(
                amount=50,
                currency="usd",
                source=token,
                description='Your Registration is successfull!')

            self.charge_id = response.id
        except self.stripe.CardError:
            return False, {'message': 'failed'}

        return True, response


#signals to create Profile when a user is created
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create( user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance, **kwargs):
    instance.profile.save()


def logged_in(sender, **kwargs):
    user = kwargs['user']
    request = kwargs['request']
    request.session['username'] = 'username'

# Connect django-allauth Signals
user_logged_in.connect(logged_in)