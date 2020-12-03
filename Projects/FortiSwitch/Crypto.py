'''Get the password'''
import keyring

SERVICE = "Dummy"

password = keyring.get_password(SERVICE, 'user') # Retrieve password
cred = keyring.get_credential(SERVICE, 'None') # Retrieve credentials

print(f"Username: {cred.username}")
print(f"Password: {cred.password}")
