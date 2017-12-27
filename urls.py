from django.urls import path
from . import views
#from cadi_config_app.views import DeviceListView
#from cadi_config_app.views import ConfigurationData
#from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('devices/', views.device_list, name='device_list'),
    path('add-device/', views.new_device_form, name='new_device'),
    path('configuration/dev/<int:device_id>/', views.configuration_data, name='configuration_data'),
    path('configuration/dev/<int:device_id>/delete', views.delete_device, name='delete_device'),
    #url(r'^configuration/(?P<pk>\d+)/$', views.configuration, name='device_detail'),

    #path('testpage', TemplateView.as_view(template_name="cadi_config_app/device-list.html")),
]