from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date


class Pet(models.Model):
    """Model representing an animal."""
    pet_name = models.CharField(max_length=100)
    pet_image = models.ImageField(upload_to='images/', null=True, blank=True)
    uploaded_user = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_pets', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_pets', blank=True)

    class Meta:
        ordering = ['pet_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular animal instance."""
        return reverse('pet_detail', args=[str(self)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.pet_name}'
