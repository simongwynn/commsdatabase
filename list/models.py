from django.db import models
from django.utils.html import format_html
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import django_tables2 as tables
from django.urls import reverse

# Create your models here.

class Event(models.Model):
    event_id = models.CharField(primary_key=True, max_length=100)
    event_name = models.CharField(max_length=150)

    def __str__(self):
        return self.event_id


class Contact(models.Model):
    contact_name = models.CharField(max_length=150)
    contact_organisation = models.CharField(max_length=150)
    contact_email = models.EmailField(max_length = 254)
    contact_mobile = PhoneField(blank=True, help_text='Mobile number')
    startlist = models.BooleanField(default=False)
    results = models.BooleanField(default=False)
    communiques = models.BooleanField(default=False)
    event = models.ForeignKey(Event,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact_name+'(Contact Only)'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event)

    def __str__(self):
        return str(self.user)

    @receiver(post_save, sender=User) #add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User) #add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()




