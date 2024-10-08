from django.db import models
from datetime import date

# Create your models here.

class Note(models.Model):
    """
    Model for creating and storing notes on Django and Python subject matter.
    Title: String, Date: NewDate, Subject: String, Content: String, Draft: Boolean
    """
    title = models.CharField(max_length=50, blank=False)
    date = models.DateField(default=date.today)
    subject = models.CharField(max_length=50, blank=False)
    content = models.TextField()
    draft = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Markdown Content"

    def __str__(self):
        return f"Note: {self.title} | {self.date} | {self.draft}"