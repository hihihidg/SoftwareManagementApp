from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

class SoftwareType(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the type of software')
    def __str__(self):
        return self.name

class Software(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, help_text='Enter a description of the software')
    softwaretype = models.ManyToManyField(SoftwareType, help_text='Select software types')

    @property
    def any_avaiable(self):
        for copy in self.softwareinstance_set.all:
            if (copy.renewal_date and date.today() <= copy.renewal_date) or copy.self.status == 'a':
                return True
        return False

    class Meta:
        permissions = (("canmake", "Abiity to add a software"),)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('software-detail', args=[str(self.id)])

class SoftwareInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this software instance')
    software = models.ForeignKey('Software', on_delete=models.CASCADE, null=True)
    renewal_date = models.DateField(null=True, blank=True)
    renewal_cost = models.FloatField()
    license_key =models.CharField(max_length=26)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS = (
        ('a', 'Available'),
        ('u', 'Unavailable'),
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='a',
    )

    @property
    def is_available(self):
        if self.status == 'a':
            return True
        return False
    @property
    def is_overdue(self):
        if self.renewal_date and date.today() > self.renewal_date:
            return True
        return False

    class Meta:
        ordering = ['renewal_date']

    def __str__(self):
        return f'{self.id} ({self.software.title})'

class RequestingSoftware(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    department = models.CharField(max_length=300)
    reason = models.TextField(max_length=1000, help_text='Enter a reason for why you need the software')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this software instance')
    software = models.ForeignKey('Software', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    send_date = models.DateField(null = True, blank= True)
    class Meta:
        ordering = ['send_date']

    def __str__(self):
        return f'{self.id} ({self.software.title})'