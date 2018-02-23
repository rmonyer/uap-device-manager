from django.db import models

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


# UAP Device model
class Device(models.Model):
    mac_address = models.CharField(max_length=17, default='00:00:00:00:00:00')
    description = models.CharField(max_length=32, default='')
    license_key = models.TextField(null=True, blank=True, editable=False)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)
    modified_by = models.TextField(null=True, blank=True, editable=False)
    enable_sp2 = models.BooleanField(default=False)
    enable_sip = models.BooleanField(default=False)
    enable_p2p = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ["-description"]

    # def __str__(self):
    #     return self.id


# UAP Configuration model
class Configuration(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, editable=False)
    module = models.CharField(max_length=3, default='ttt')
    parameter = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)

    # def __str__(self):
    #     return self.parameter


# Opened/Current Device Configuration
class ActiveDevice(models.Model):
    device_id = models.PositiveIntegerField(default=0)
    mac_address = models.CharField(max_length=17, default='00:00:00:00:00:00')
    description = models.CharField(max_length=32, default='')
    module = models.CharField(max_length=3, default='ttt')
    uap_networkmode = models.CharField(max_length=6, choices=NETWORKMODE_CHOICES, default='dhcp')
    uap_ipaddress = models.GenericIPAddressField()
    uap_netmask = models.GenericIPAddressField()
    uap_gateway = models.GenericIPAddressField()
    uap_handsetpresent = models.BooleanField()
    uap_externalspeakerconnected = models.BooleanField()
    uap_camerapresent = models.BooleanField()
    uap_ntpserveraddr = models.GenericIPAddressField()
    uap_dnsaddrprimary = models.GenericIPAddressField()
    uap_dnsaddrsecondary = models.GenericIPAddressField()
    uap_homemode = models.CharField(max_length=3, default='ttt')
    sp2_enabled = models.BooleanField()
    sp2_groupid = models.TextField(null=True, blank=True)
    sp2_stationid = models.TextField(null=True, blank=True)
    sip_enable = models.BooleanField()
    sip_sipreg1 = models.GenericIPAddressField()
    sip_sipreg2 = models.GenericIPAddressField()
    sip_sipreg3 = models.GenericIPAddressField()
    sip_sipaccount = models.TextField(null=True, blank=True)
    sip_sippw1 = models.CharField(max_length=15, null=True, blank=True)
    sip_sippw2 = models.CharField(max_length=15, null=True, blank=True)
    sip_sippw3 = models.CharField(max_length=15, null=True, blank=True)
    sip_sipport = models.PositiveSmallIntegerField()
    sip_regtimeout = models.PositiveSmallIntegerField()
    sip_keepaliveinterval = models.PositiveSmallIntegerField()
    p2p_enabled = models.BooleanField()
    p2p_mode = models.CharField(max_length=6, choices=P2PMODE_CHOICES, default='MODE1')
    p2p_displayname = models.CharField(max_length=15)
    p2p_survailmode = models.CharField(max_length=6, choices=P2PSURVAILMODE_CHOICES, default='0')
