import keyring

# the service is just a namespace for your app
service_id = 'IM_YOUR_APP!'

keyring.set_password(service_id, 'dustin', 'my secret password')
password = keyring.get_password(service_id, 'dustin') # retrieve password