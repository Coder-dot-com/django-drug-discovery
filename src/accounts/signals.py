from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile
# from ai.models import UserAI

# from tiers.models import Tier, UserTier

# from subscriptions.models import UserPaymentStatus


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        # profile.beta_tester = True
        profile.save()

        # free_tier = Tier.objects.filter(type="free_tier").first()

        # UserTier.objects.create(user=user, tier=free_tier)

        # UserAI.objects.create(user=user, monthly_ai_credits_remaining=free_tier.monthly_ai_credits)
        
        # if not user.is_staff:
        #     UserPaymentStatus.objects.create(user=user, status="free")







    