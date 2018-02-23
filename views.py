from django.shortcuts import get_list_or_404, render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .forms import DeviceForm, UAPForm, SIPForm, SP2Form, P2PForm
from .models import Device, ActiveDevice, Configuration


def home(request):
    return render(request, "cadi_config_app/index.html")


# device list view
@login_required(login_url='/admin/login/')
def device_list(request):
    all_devices_list = Device.objects.order_by('description')  # [:5]
    context = {'all_devices_list': all_devices_list}
    return render(request, 'cadi_config_app/device_list.html', context)  # {'form': form})


# add new device form
@login_required(login_url='/admin/login/')
def new_device_form(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.modified_by = request.user
            device.save()

            # Create new Configuration records for each parameter with defaults
            config_param = Configuration.objects.create(module="UAP", parameter="NetworkMode", value="static",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="IPaddress", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="Netmask", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="Gateway", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="HandsetPresent", value="False",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="ExternalSpeakerConnected",
                                                        value="False", device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="CameraPresent", value="False",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="NTPServerAddr", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="DNSaddrPrimary", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="DNSaddrSecondary", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="UAP", parameter="HomeMode", value="0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SP2", parameter="Enabled", value=device.enable_sp2,
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SP2", parameter="GroupID", value="000",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SP2", parameter="StationID", value="000",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="Enabled", value=device.enable_sip,
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPreg1", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPreg2", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPreg3", value="0.0.0.0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPaccount", value="",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPpw1", value="", device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPpw2", value="", device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPpw3", value="", device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="SIPport", value="0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="RegTimeout", value="0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="SIP", parameter="KeepAliveInterval", value="0",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="P2P", parameter="Enabled", value=device.enable_p2p,
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="P2P", parameter="Mode", value="MODE1",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="P2P", parameter="DisplayName", value="",
                                                        device_id=device.pk)
            config_param = Configuration.objects.create(module="P2P", parameter="SurvailMode", value="0",
                                                        device_id=device.pk)

            return redirect('configuration_data', device_id=device.pk)
    else:
        form = DeviceForm()

    return render(request, 'cadi_config_app/new_device.html', {'form': form})


# configuration data view
@login_required(login_url='/admin/login/')
def configuration_data(request, device_id):
    configuration_filter = Configuration.objects.filter(device_id=device_id)
    device_filter = Device.objects.get(pk=device_id)

    ConfigurationUAPFormSet = modelformset_factory(ActiveDevice, form=UAPForm)
    ConfigurationSP2FormSet = modelformset_factory(ActiveDevice, form=SP2Form)
    ConfigurationSIPFormSet = modelformset_factory(ActiveDevice, form=SIPForm)
    ConfigurationP2PFormSet = modelformset_factory(ActiveDevice, form=P2PForm)

    if request.method == 'POST':
        uapformset = ConfigurationUAPFormSet(request.POST, request.FILES,
                                             queryset=ActiveDevice.objects.filter(device_id=device_id))
        if uapformset.is_valid():
            uapformset.save()
            # return redirect('device_list')

        sp2formset = ConfigurationSP2FormSet(request.POST, request.FILES,
                                             queryset=ActiveDevice.objects.filter(device_id=device_id))
        if sp2formset.is_valid():
            sp2formset.save()
            # return redirect('device_list')

        sipformset = ConfigurationSIPFormSet(request.POST, request.FILES,
                                             queryset=ActiveDevice.objects.filter(device_id=device_id))
        if sipformset.is_valid():
            sipformset.save()
            # return redirect('device_list')

        p2pformset = ConfigurationP2PFormSet(request.POST, request.FILES,
                                             queryset=ActiveDevice.objects.filter(device_id=device_id))
        if p2pformset.is_valid():
            p2pformset.save()
            # return redirect('device_list')

        # Copy fields from the ActiveDevice record to the current Configuration record
        # ...
    else:
        # Delete any left over records in the ActiveDevice table
        deleteactivedevices = ActiveDevice.objects.all()
        deleteactivedevices.delete()

        # Copy fields from current Device & Configuration record to a new ActiveDevice record
        copyparam = ActiveDevice(device_id=device_id, mac_address=device_filter.mac_address,
                                 description=device_filter.description,
                                 uap_networkmode=configuration_filter.get(module="UAP", parameter='NetworkMode').value,
                                 uap_ipaddress=configuration_filter.get(module="UAP", parameter='IPaddress').value,
                                 uap_netmask=configuration_filter.get(module="UAP", parameter='Netmask').value,
                                 uap_gateway=configuration_filter.get(module="UAP", parameter='Gateway').value,
                                 uap_handsetpresent=configuration_filter.get(module="UAP",
                                                                             parameter='HandsetPresent').value,
                                 uap_externalspeakerconnected=configuration_filter.get(module="UAP",
                                                                                       parameter='ExternalSpeakerConnected').value,
                                 uap_camerapresent=configuration_filter.get(module="UAP",
                                                                            parameter='CameraPresent').value,
                                 uap_ntpserveraddr=configuration_filter.get(module="UAP",
                                                                            parameter='NTPServerAddr').value,
                                 uap_dnsaddrprimary=configuration_filter.get(module="UAP",
                                                                             parameter='DNSaddrPrimary').value,
                                 uap_dnsaddrsecondary=configuration_filter.get(module="UAP",
                                                                               parameter='DNSaddrSecondary').value,
                                 uap_homemode=configuration_filter.get(module="UAP", parameter='HomeMode').value,
                                 sp2_enabled=configuration_filter.get(module="SP2", parameter='Enabled').value,
                                 sp2_groupid=configuration_filter.get(module="SP2", parameter='GroupID').value,
                                 sp2_stationid=configuration_filter.get(module="SP2", parameter='StationID').value,
                                 sip_enable=configuration_filter.get(module="SIP", parameter='Enabled').value,
                                 sip_sipreg1=configuration_filter.get(module="SIP", parameter='SIPreg1').value,
                                 sip_sipreg2=configuration_filter.get(module="SIP", parameter='SIPreg2').value,
                                 sip_sipreg3=configuration_filter.get(module="SIP", parameter='SIPreg3').value,
                                 sip_sipaccount=configuration_filter.get(module="SIP", parameter='SIPaccount').value,
                                 sip_sippw1=configuration_filter.get(module="SIP", parameter='SIPpw1').value,
                                 sip_sippw2=configuration_filter.get(module="SIP", parameter='SIPpw2').value,
                                 sip_sippw3=configuration_filter.get(module="SIP", parameter='SIPpw3').value,
                                 sip_sipport=configuration_filter.get(module="SIP", parameter='SIPport').value,
                                 sip_regtimeout=configuration_filter.get(module="SIP", parameter='RegTimeout').value,
                                 sip_keepaliveinterval=configuration_filter.get(module="SIP",
                                                                                parameter='KeepAliveInterval').value,
                                 p2p_enabled=configuration_filter.get(module="P2P", parameter='Enabled').value,
                                 p2p_mode=configuration_filter.get(module="P2P", parameter='Mode').value,
                                 p2p_displayname=configuration_filter.get(module="P2P", parameter='DisplayName').value,
                                 p2p_survailmode=configuration_filter.get(module="P2P", parameter='SurvailMode').value,
                                 )
        copyparam.save()

        uapformset = ConfigurationUAPFormSet(queryset=ActiveDevice.objects.filter(device_id=device_id))
        sp2formset = ConfigurationSP2FormSet(queryset=ActiveDevice.objects.filter(device_id=device_id))
        sipformset = ConfigurationSIPFormSet(queryset=ActiveDevice.objects.filter(device_id=device_id))
        p2pformset = ConfigurationP2PFormSet(queryset=ActiveDevice.objects.filter(device_id=device_id))
    return render(request, 'cadi_config_app/configuration_data.html', {
        'uapformset': uapformset,
        'sp2formset': sp2formset,
        'sipformset': sipformset,
        'p2pformset': p2pformset,
    })
    # return render(request, 'cadi_config_app/configuration_data.html', {'formset': formset})


# delete device view
@login_required(login_url='/admin/login/')
def delete_device(request, device_id):
    if Configuration.objects.filter(device_id=device_id).count() > 0:
        config_rows = Configuration.objects.filter(device_id=device_id)
        config_rows.delete()

    if Device.objects.filter(pk=device_id).count() > 0:
        the_device = Device.objects.filter(pk=device_id)
        the_device.delete()

    all_devices_list = Device.objects.order_by('description')  # [:5]
    context = {'all_devices_list': all_devices_list}
    return render(request, 'cadi_config_app/device_list.html', context)

# configuration data view
# @login_required(login_url='/admin/login/')
# def configuration_data(request, device_id):
#     # config_params = Configuration.objects.filter(device_id=device_id)
#     ConfigurationFormSet = modelformset_factory(Configuration, form=ConfigurationForm, max_num=29)
#     if request.method == 'POST':
#         formset = ConfigurationFormSet(request.POST, request.FILES, queryset=Configuration.objects.filter(device_id=device_id))
#         if formset.is_valid():
#             formset.save()
#             return redirect('device_list')
#     else:
#         formset = ConfigurationFormSet(queryset=Configuration.objects.filter(device_id=device_id))
#     return render(request, 'cadi_config_app/configuration_data.html', {'formset': formset})
