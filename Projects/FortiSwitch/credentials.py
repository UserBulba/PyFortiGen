import os

def getCredentials():
    import base64

    splitter='<PC+,DFS/-SHQ.R'
    directory='C:\\Temp\\Python'

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(directory+'\\Credentials.txt', 'r') as file:
            cred = file.read()
            file.close()
    except:
        print('I could not file the credentials file. \nSo I dont keep asking you for your name and password everytime you run me, I will be saving an encrypted file at {}.\n'.format(directory))

        lanid = base64.b64encode(bytes(input('   LanID: '), encoding='utf-8')).decode('utf-8')
        name = base64.b64encode(bytes(input('   Name: '), encoding='utf-8')).decode('utf-8')
        password = base64.b64encode(bytes(input('   Pass: '), encoding='utf-8')).decode('utf-8')
        cred = lanid+splitter+name+splitter+password
        with open(directory+'\\Credentials.txt','w+') as file:
            file.write(cred)
            file.close()

    return {'lanid':base64.b64decode(bytes(cred.split(splitter)[0], encoding='utf-8')).decode('utf-8'),
            'name':base64.b64decode(bytes(cred.split(splitter)[1], encoding='utf-8')).decode('utf-8'),
            'password':base64.b64decode(bytes(cred.split(splitter)[2], encoding='utf-8')).decode('utf-8')}

def updateCredentials():
    import base64

    splitter='<PC+,DFS/-SHQ.R'
    directory='C:\\Temp\\Python'

    if not os.path.exists(directory):
        os.makedirs(directory)

    print('I will be saving an encrypted file at {}.\n'.format(directory))

    lanid = base64.b64encode(bytes(input('   LanID: '), encoding='utf-8')).decode('utf-8')
    name = base64.b64encode(bytes(input('   Name: '), encoding='utf-8')).decode('utf-8')
    password = base64.b64encode(bytes(input('   Pass: '), encoding='utf-8')).decode('utf-8')
    cred = lanid+splitter+name+splitter+password
    with open(directory+'\\Credentials.txt','w+') as file:
        file.write(cred)
        file.close()

def create_key_credentials():
    import keyring

    directory='C:\\Temp\\Python'

    if not os.path.exists(directory):
        os.makedirs(directory)
# cred = getCredentials()
# updateCredentials()
