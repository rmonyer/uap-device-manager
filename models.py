from django.db import models

# Define Managers for each module type (UAP, SP2, SIP, and P2P)
# class UAPManager(models.Manager):
#     def get_queryset(self):
#         return super(UAPManager, self).get_queryset().filter(module='UAP')

# class SP2Manager(models.Manager):
#     def get_queryset(self):
#         return super(SP2Manager, self).get_queryset().filter(module='SP2')

# class SIPManager(models.Manager):
#     def get_queryset(self):
#         return super(SIPManager, self).get_queryset().filter(module='SIP')

# class P2PManager(models.Manager):
#     def get_queryset(self):
#         return super(P2PManager, self).get_queryset().filter(module='P2P')


# CADi Device model
class Device(models.Model):
    mac_address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
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


# CADi Configuration model
class Configuration(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, editable=False)
    module = models.TextField(null=True, blank=True)
    parameter = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    input_type = models.TextField(null=True, blank=True, editable=False)
    input_options = models.TextField(null=True, blank=True, editable=False)

    # def __str__(self):
    #     return self.parameter

    # configs = models.Manager()
    # uap = UAPManager()
    # sp2 = SP2Manager()
    # sip = SIPManager()
    # p2p = P2PManager()
