import keyring

# the service is just a namespace for your app
Service = 'FortiSwitch'

# keyring.set_password(service_id, 'dustin', 'my secret password')
#password = keyring.get_password(service_id, 'dustin') # retrieve password
#c = keyring.get_credential(service_id, 'None')

#print (c['username'])
#print (c['password'])

cred = keyring.get_credential(Service, 'None')
print(f"Username: {cred.username}")
print(f"Password: {cred.password}")