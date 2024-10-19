from django.db import models
#Create your models here. We make classes to create models that we can create afterwards in the GUI

NETMIKO_MAPPING = {
    'cisco_ios': 'cisco_ios',
    'cisco_iosxe': 'cisco_ios',
}

NAPALM_MAPPING = {
    'cisco_ios': 'ios',
    'cisco_iosxe': 'ios',
}

class Device(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=70)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True)
    secret = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(
        max_length=30, choices=(("router", "Router"), ("switch", "Switch"), ("firewall", "Firewall")), blank=True
    )
 
    platform = models.CharField(
        max_length=30, choices=(("cisco_ios", "Cisco IOS"), ("cisco_iosxe", "Cisco IOS XE")), blank=True
    )
    
    def __str__(self) -> str:
        return self.name
    @property
    def napalm_driver(self) -> str:
        return NAPALM_MAPPING[self.platform]
    @property
    def netmiko_device_type(self) -> str:
        return NETMIKO_MAPPING[self.platform]
    



