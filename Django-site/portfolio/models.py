from django.db import models

# Create your models here.

class MyNotes(models.Model):
    """
    Model for creating and storing notes on Django and Python subject matter.
    Title: String, Date: NewDate, Subject: String, Content: String, Draft: Boolean
    """
    title = models.CharField(max_length=50, blank=False)
    date = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=50, blank=False)
    content = models.TextField()
    draft = models.BooleanField(default=True)

