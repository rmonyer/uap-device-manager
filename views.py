from django.shortcuts import get_list_or_404, render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .forms import DeviceForm, ConfigurationForm
from .models import Device, Configuration

config_uap_fields = ["NetworkMode", "IPaddress", "Netmask", "Gateway", "HandsetPresent", "ExternalSpeakerConnected",
                        "CameraPresent", "NTPServerAddr", "DNSaddrPrimary", "DNSaddrSecondary", "HomeMode"]
config_sp2_fields = ["Enabled", "GroupID", "StationID"]
config_sip_fields = ["Enabled", "SIPreg1", "SIPreg2", "SIPreg3", "SIPaccount", "SIPpw1",
                        "SIPpw2", "SIPpw3", "SIPport", "RegTimeout", "KeepAliveInterval"]
config_p2p_fields = ["Enabled", "Mode", "DisplayName", "SurvailMode"]

def home(request):
    return render(request, "cadi_config_app/index.html")

# device list view
@login_required(login_url='/admin/login/')
def device_list(request):
    all_devices_list = Device.objects.order_by('description')   #[:5]
    context = {'all_devices_list': all_devices_list}
    return render(request, 'cadi_config_app/device_list.html', context) # {'form': form})

# add new device form
@login_required(login_url='/admin/login/')
def new_device_form(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.modified_by = request.user
            device.save()
            
            for new_field in config_uap_fields:
                config_param = Configuration(module="UAP", parameter=new_field, value="", input_type="", input_options="", device_id=device.pk)
                config_param.save()

            for new_field in config_sp2_fields:
                if new_field == 'Enabled':
                    config_param = Configuration(module="SP2", parameter=new_field, value=device.enable_sp2, input_type="", input_options="", device_id=device.pk)
                else:
                    config_param = Configuration(module="SP2", parameter=new_field, value="", input_type="", input_options="", device_id=device.pk)
                config_param.save()

            for new_field in config_sip_fields:
                if new_field == 'Enabled':
                    config_param = Configuration(module="SIP", parameter=new_field, value=device.enable_sip, input_type="", input_options="", device_id=device.pk)
                else:
                    config_param = Configuration(module="SIP", parameter=new_field, value="", input_type="", input_options="", device_id=device.pk)
                config_param.save()

            for new_field in config_p2p_fields:
                if new_field == 'Enabled':
                    config_param = Configuration(module="P2P", parameter=new_field, value=device.enable_p2p, input_type="", input_options="", device_id=device.pk)
                else:
                    config_param = Configuration(module="P2P", parameter=new_field, value="", input_type="", input_options="", device_id=device.pk)
                config_param.save()

            return redirect('configuration_data', device_id=device.pk)
    else:
        form = DeviceForm()

    return render(request, 'cadi_config_app/new_device.html', {'form': form})


# configuration data view
@login_required(login_url='/admin/login/')
def configuration_data(request, device_id):
    # config_params = Configuration.objects.filter(device_id=device_id)
    ConfigurationFormSet = modelformset_factory(Configuration, form=ConfigurationForm, max_num=29)
    if request.method == 'POST':
        formset = ConfigurationFormSet(request.POST, request.FILES, queryset=Configuration.objects.filter(device_id=device_id))
        if formset.is_valid():
            formset.save()
            return redirect('device_list')
    else:
        formset = ConfigurationFormSet(queryset=Configuration.objects.filter(device_id=device_id))
    return render(request, 'cadi_config_app/configuration_data.html', {'formset': formset})

# delete device view
@login_required(login_url='/admin/login/')
def delete_device(request, device_id):
    if Configuration.objects.filter(device_id=device_id).count() > 0:
        config_rows = Configuration.objects.filter(device_id=device_id)
        config_rows.delete()

    if Device.objects.filter(pk=device_id).count() > 0:
        the_device = Device.objects.filter(pk=device_id)
        the_device.delete()

    all_devices_list = Device.objects.order_by('description')   #[:5]
    context = {'all_devices_list': all_devices_list}
    return render(request, 'cadi_config_app/device_list.html', context)
