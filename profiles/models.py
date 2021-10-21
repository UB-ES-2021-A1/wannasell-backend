from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return 'static/images/avatars/{0}/{1}'.format(instance.user.id, filename)


# Define account model extras here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='static/images/default/avatar/default.png')
    bio = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=1024, blank=True)

    class Meta:
        permissions = (
            ('modify_other_profiles', 'Allows the user to modify other profiles (Admin Access)'),
        )
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
