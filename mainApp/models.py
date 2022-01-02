from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class ItemDetail(models.Model):
    status = (
        ('Found', 'Found'),
        ('Lost', 'Lost')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Item Name')
    location = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(verbose_name='Item Details')
    item_status = models.CharField(choices=status, default='Lost', max_length=30, verbose_name='Items Status', null=True)
    dateFL = models.DateField(verbose_name='Date Found/Lost')
    image = models.ImageField(upload_to='images/', verbose_name='Item Image')
    timeAdded = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-timeAdded']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemDetail, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Message')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
