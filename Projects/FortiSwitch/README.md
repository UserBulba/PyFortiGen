## Install requirements :

```powershell
py -m pip install -r requirements.txt
```

## Set Password :

Both methods works the same way.

 - Python method :

```python
import keyring
keyring.set_password('Dummy', 'user', 'password')
```

---

- Powershell method :

```powershell
Import-Module CredentialManager
New-StoredCredential -Target Dummy -UserName user -Password "password" -Comment "My password for..." -Type Generic -Persist Enterprise
```