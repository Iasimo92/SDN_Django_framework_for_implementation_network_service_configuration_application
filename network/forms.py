from django import forms

class DeviceConfigForm(forms.Form):
    hostname = forms.CharField(label='Device Hostname', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    interface = forms.CharField(label='Interface', max_length=50)
    ip_address = forms.GenericIPAddressField(label='IP Address')
    subnet_mask = forms.GenericIPAddressField(label='Subnet Mask')