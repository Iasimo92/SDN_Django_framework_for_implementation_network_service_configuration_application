from django.test import TestCase
from django.urls import reverse
from .models import Device

class DeviceViewTests(TestCase):

    def setUp(self):
        # Set up a test device
        self.device = Device.objects.create(
            host='192.168.56.140',
            username='admin',
            password='password',
            platform='cisco_ios',
            name='Test Device'
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))  # Adjust the name to your URL pattern
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Controller')

    def test_get_device_stats(self):
        response = self.client.get(reverse('get_device_stats', args=[self.device.id]))
        self.assertEqual(response.status_code, 200)
