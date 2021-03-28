# FortiSwitch SNMP configuration

This tool allows you to automate SNMP configuration on FortiSwitch devices.

## Install requirements

```powershell
py -m pip install -r requirements.txt
```

## Set Password

For further use it's possible to save password in windows credential manager.
However, if you don't want to dwell on security issues like storing credentials in plain text, use the option base on conf.ini

Both methods works the same way.

### Credential Manager

- Python method :

```python
import keyring
keyring.set_password('service', 'user', 'password')
```

---

- Powershell method :

```powershell
Import-Module CredentialManager
New-StoredCredential -Target Dummy -UserName user -Password "password" -Comment "My password for..." -Type Generic -Persist Enterprise

Get-StoredCredential -Target Dummy -AsCredentialObject
```
