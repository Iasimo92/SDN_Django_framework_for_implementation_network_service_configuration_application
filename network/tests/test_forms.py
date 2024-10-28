from django.test import TestCase
from ..forms import DeviceConfigForm  # Correct import statement

class DeviceConfigFormTest(TestCase):

    def setUp(self):
        # Common setup for each test
        self.valid_data = {
            'hostname': 'TestDevice',
            'username': 'admin',
            'password': 'securepassword',
            'interface': 'GigabitEthernet0/1',
            'ip_address': '192.168.1.1',
            'subnet_mask': '255.255.255.0'
        }

    def tearDown(self):
        # Clean up if needed after each test
        pass  # Placeholder for any teardown logic, like closing connections

    def test_form_valid_data(self):
        # Use setUp's valid data for a test
        form = DeviceConfigForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['hostname'], 'TestDevice')

    def test_form_invalid_ip_address(self):
        # Use setUp's valid data but change IP address to invalid
        invalid_data = self.valid_data.copy()
        invalid_data['ip_address'] = '192.168.1.256'  # Invalid IP

        form = DeviceConfigForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('ip_address', form.errors)

    def test_form_blank_password(self):
        # Use setUp's valid data but leave password blank
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = ''  # Blank password

        form = DeviceConfigForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
