from django.db import models
from django.urls import reverse

# Create your models here.
class Calendar(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event:detail', args=[str(self.id)])
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="post/%Y/%b/%d/", null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ()

    def __str__(self):
        return self.title
    
class VolunteerRequest(models.Model):
    name = models.EmailField(blank=True)
    email = models.EmailField(unique=True, blank=True)
    message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ()

    def __str__(self):
        return self.name