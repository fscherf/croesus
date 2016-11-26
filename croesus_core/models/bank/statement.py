from django.db import models

__all__ = [
    'Statement',
]


class Statement(models.Model):
    data = models.TextField()

    format = models.CharField(max_length=16)
    file_name = models.CharField(max_length=128, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(blank=True, null=True)
