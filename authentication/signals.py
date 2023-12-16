from django.db.models import signals
from django.dispatch import receiver
from .models import User,Profile

@receiver(signals.post_save,sender=User)
def create_user_profile(sender,**kwargs):
    if kwargs['created']:
         Profile.objects.create(user=kwargs['instance'])