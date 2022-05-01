from .models import RequestingSoftware, Software, SoftwareType, SoftwareInstance
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import SoftwareInstance

class ApplyLicenseKeyForm(forms.ModelForm):
    def __init__(self, mysoftware, *args, **kwargs):
        super(ApplyLicenseKeyForm, self).__init__(*args, **kwargs)
        self.fields['license_key'] = forms.ModelChoiceField(queryset = SoftwareInstance.objects.filter(software = mysoftware), to_field_name='license_key')
    class Meta:
        model = SoftwareInstance
        fields = ('license_key', )
