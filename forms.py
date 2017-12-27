from django import forms
# from django.utils.translation import gettext_lazy as _
from .models import Device, Configuration
from sys import stderr

def print_err(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

class DeviceForm(forms.ModelForm):
    description = forms.CharField(
        max_length=50,
        required=True,
        #widget=forms.Textarea(),
        help_text='Enter a unique description'
    )
    mac_address = forms.CharField(
        max_length=17,
        required=True,
        #widget=forms.Textarea(),
        help_text='Enter the unique MAC address'
    )
    enable_sp2 = forms.BooleanField()
    enable_sip = forms.BooleanField()
    enable_p2p = forms.BooleanField()

    class Meta:
        model = Device
        fields = ('description', 'mac_address', 'enable_sp2', 'enable_sip', 'enable_p2p')

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.css_class = "device"
        self.fields['mac_address'].label = 'MAC Address'
        self.fields['enable_sp2'].label = 'SP2 Enabled'
        self.fields['enable_sip'].label = 'SIP Enabled'
        self.fields['enable_p2p'].label = 'P2P Enabled'

    def clean(self):
        cleaned_data = super(DeviceForm, self).clean()
        description = cleaned_data.get('description')
        mac_address = cleaned_data.get('mac_address')
        if not description and not mac_address:
            raise forms.ValidationError('You must enter the Description and MAC Address for the new CADi device.')

class ConfigurationForm(forms.ModelForm):
    # parameter = forms.CharField()
    value = forms.CharField(max_length=20)

    class Meta:
        model = Configuration
        fields = ('value',)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            # print_err()
            self.fields['value'].label = kwargs['instance'].parameter   # this overrides the label for the value field with the text stored in the parameter field

    def clean(self):
        cleaned_data = super(ConfigurationForm, self).clean()
        value = cleaned_data.get('value')
        if not value:
            raise forms.ValidationError('You must enter a value!')
    
