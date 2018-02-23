from django import forms
# from django.utils.translation import gettext_lazy as _
from .models import Device, ActiveDevice    #Configuration
from sys import stderr

NETWORKMODE_CHOICES = (
    ('static', 'Static'),
    ('dhcp', 'DHCP'),
)

P2PMODE_CHOICES = (
    ('MODE1', 'Mode One'),
    ('MODE2', 'Mode Two'),
    ('MODE3', 'Mode Three'),
    ('MODE4', 'Mode Four'),
)

P2PSURVAILMODE_CHOICES = (
    ('0', 'OFF'),
    ('1', 'Audio'),
    ('2', 'Video'),
    ('3', 'Audio/Video'),
)

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

class UAPForm(forms.ModelForm):
    # parameter = forms.CharField()
    mac_address = forms.CharField(max_length=17)
    description = forms.CharField(max_length=32)
    uap_networkmode = forms.ChoiceField(choices=NETWORKMODE_CHOICES)
    uap_ipaddress = forms.GenericIPAddressField()
    uap_netmask = forms.GenericIPAddressField()
    uap_gateway = forms.GenericIPAddressField()
    uap_handsetpresent = forms.BooleanField()
    uap_externalspeakerconnected = forms.BooleanField()
    uap_camerapresent = forms.BooleanField()
    uap_ntpserveraddr = forms.GenericIPAddressField()
    uap_dnsaddrprimary = forms.GenericIPAddressField()
    uap_dnsaddrsecondary = forms.GenericIPAddressField()
    uap_homemode = forms.IntegerField()

    class Meta:
        model = ActiveDevice
        fields = ('mac_address', 'description', 'uap_networkmode', 'uap_ipaddress', 'uap_netmask', 'uap_gateway',
                    'uap_handsetpresent', 'uap_externalspeakerconnected', 'uap_camerapresent', 'uap_ntpserveraddr', 'uap_dnsaddrprimary',
                    'uap_dnsaddrsecondary', 'uap_homemode',)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.css_class = "activedevice"
        self.fields['mac_address'].label = 'MAC Address'
        self.fields['uap_networkmode'].label = 'Network Mode'
        self.fields['uap_ipaddress'].label = 'IP Address'
        self.fields['uap_netmask'].label = 'Netmask'
        self.fields['uap_gateway'].label = 'Gateway'
        self.fields['uap_handsetpresent'].label = 'Handset Present'
        self.fields['uap_externalspeakerconnected'].label = 'External Speaker Connected'
        self.fields['uap_camerapresent'].label = 'Camera Present'
        self.fields['uap_ntpserveraddr'].label = 'NTP Server Address'
        self.fields['uap_dnsaddrprimary'].label = 'Primary DNS Server'
        self.fields['uap_dnsaddrsecondary'].label = 'Secondary DNS Server'
        self.fields['uap_homemode'].label = 'Home Mode'

    def clean(self):
        cleaned_data = super(UAPForm, self).clean()
        value = cleaned_data.get('value')
        if not value:
            raise forms.ValidationError('You must enter a value!')

class SP2Form(forms.ModelForm):
    # parameter = forms.CharField()
    sp2_enabled = forms.BooleanField()
    sp2_groupid = forms.CharField(max_length=10)
    sp2_stationid = forms.CharField(max_length=10)

    class Meta:
        model = ActiveDevice
        fields = ('sp2_enabled', 'sp2_groupid', 'sp2_stationid',)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.css_class = "activedevice"
        self.fields['sp2_enabled'].label = 'SP2 Enabled'
        self.fields['sp2_groupid'].label = 'Group ID'
        self.fields['sp2_stationid'].label = 'Station ID'

    def clean(self):
        cleaned_data = super(SP2Form, self).clean()
        value = cleaned_data.get('value')
        if not value:
            raise forms.ValidationError('You must enter a value!')


class SIPForm(forms.ModelForm):
    # parameter = forms.CharField()
    sip_enable = forms.BooleanField()
    sip_sipaccount = forms.CharField(max_length=32)
    sip_sipport = forms.IntegerField()
    sip_sipreg1 = forms.GenericIPAddressField()
    sip_sippw1 = forms.PasswordInput()
    sip_sipreg2 = forms.GenericIPAddressField()
    sip_sippw2 = forms.PasswordInput()
    sip_sipreg3 = forms.GenericIPAddressField()
    sip_sippw3 = forms.PasswordInput()
    sip_regtimeout = forms.IntegerField()
    sip_keepaliveinterval = forms.IntegerField()

    class Meta:
        model = ActiveDevice
        fields = ('sip_enable', 'sip_sipaccount', 'sip_sipport', 'sip_sipreg1', 'sip_sippw1', 'sip_sipreg2', 'sip_sippw2',
                    'sip_sipreg3', 'sip_sippw3', 'sip_regtimeout', 'sip_keepaliveinterval',)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.css_class = "activedevice"
        self.fields['sip_enable'].label = 'SIP Enabled'
        self.fields['sip_sipaccount'].label = 'Account'
        self.fields['sip_sipport'].label = 'Port'
        self.fields['sip_sipreg1'].label = 'Registrar 1'
        self.fields['sip_sipreg2'].label = 'Registrar 2'
        self.fields['sip_sipreg3'].label = 'Registrar 3'
        self.fields['sip_sippw1'].label = 'Password 1'
        self.fields['sip_sippw2'].label = 'Password 2'
        self.fields['sip_sippw3'].label = 'Password 3'
        self.fields['sip_regtimeout'].label = 'Registration Timeout'
        self.fields['sip_keepaliveinterval'].label = 'Keep Alive Interval'

    def clean(self):
        cleaned_data = super(SIPForm, self).clean()
        value = cleaned_data.get('value')
        if not value:
            raise forms.ValidationError('You must enter a value!')


class P2PForm(forms.ModelForm):
    # parameter = forms.CharField()
    p2p_enabled = forms.BooleanField()
    p2p_mode = forms.ChoiceField(choices=P2PMODE_CHOICES)
    p2p_displayname = forms.CharField(max_length=15)
    p2p_survailmode = forms.ChoiceField(choices=P2PSURVAILMODE_CHOICES)

    class Meta:
        model = ActiveDevice
        fields = ('p2p_enabled', 'p2p_mode', 'p2p_displayname', 'p2p_survailmode',)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.css_class = "activedevice"
        self.fields['p2p_enabled'].label = 'P2P Enabled'
        self.fields['p2p_mode'].label = 'Mode'
        self.fields['p2p_displayname'].label = 'Display Name'
        self.fields['p2p_survailmode'].label = 'Survail Mode'

    def clean(self):
        cleaned_data = super(P2PForm, self).clean()
        value = cleaned_data.get('value')
        if not value:
            raise forms.ValidationError('You must enter a value!')

# class ConfigurationForm(forms.ModelForm):
#     # parameter = forms.CharField()
#     value = forms.CharField(max_length=20)
#
#     class Meta:
#         model = Configuration
#         fields = ('value',)
#
#     def __init__(self, *args, **kwargs):
#         super(forms.ModelForm, self).__init__(*args, **kwargs)
#         if kwargs.get('instance'):
#             # print_err()
#             self.fields['value'].label = kwargs['instance'].parameter   # this overrides the label for the value field with the text stored in the parameter field
#
#     def clean(self):
#         cleaned_data = super(ConfigurationForm, self).clean()
#         value = cleaned_data.get('value')
#         if not value:
#             raise forms.ValidationError('You must enter a value!')
#

