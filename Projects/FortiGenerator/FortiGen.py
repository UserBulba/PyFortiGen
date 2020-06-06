import os
import sys
import pandas as pd

class FortiGen():
    
    Sort = []
    
    def __init__(self, Host, Wan, Lan, Gateway, DHCPStart=2, DHCPEnd=100):
        self.Host = Host
        self.Wan = Wan
        self.Lan = Lan
        self.DHCPStart = DHCPStart
        self.DHCPEnd = DHCPEnd
        self.Gateway = Gateway
        self.TimeZone = '29'
        self.Path = os.getcwd()
        self.Sys = os.path.join(self.Path, self.Host)

        FortiGen.Sort.append(self)

    def FileVerify(self):
        Error = 0
        try:
            if not os.path.exists(os.path.join(self.Path, self.Host)):
                os.makedirs(os.path.join(self.Path, self.Host))
            else:
                print ("Catalogue for device {} found".format(self.Host))
                Error =+ 1
        except:
            print ("Sorry, error occurred :",sys.exc_info()[0])
            #Count errors, to continue in loop
            Error =+ 1
            
        return Error

    def Replace(self):

        Subnet = self.Lan.split(' ')
        LanIP = (Subnet[0]).split('.')

        DHCPStartAddress = (LanIP[0] + '.'+ LanIP[1] + '.' + LanIP[2] + str(self.DHCPStart))
        DHCPEndAddress = (LanIP[0] + '.'+ LanIP[1] + '.' + LanIP[2] + str(self.DHCPEnd))

        with open(os.path.join(self.Path,'FortiConfig','DHCP.txt')) as Config:
            newText = Config.read().replace('FW502R5618001244',self.Host)
            newText = newText.replace('set timezone 04','set timezone ' + self.TimeZone)
            newText = newText.replace('set ip 10.10.20.1 255.255.255.0','set ip ' + self.Lan)
            newText = newText.replace('set default-gateway 10.10.20.1','set default-gateway ' + Subnet[0])
            newText = newText.replace('set start-ip 10.10.20.2','set start-ip ' + DHCPStartAddress)
            newText = newText.replace('set end-ip 10.10.20.254','set end-ip ' + DHCPEndAddress)
            newText = newText.replace('set ip 91.226.50.102 255.255.248.0', 'set ip ' + self.Wan)
            newText = newText.replace('set gateway 91.226.50.97', 'set gateway ' + self.Gateway)

        with open(os.path.join(self.Sys,'fgt_config.conf'), "w") as Config:
            Config.write(newText)       

        return

    def Main(self):
        if self.Wan == 'DHCP':
            CountError = self.FileVerify()
            
            
            print ('DHCP configuration :', self.Wan, "-"*3, self.Host)

            if CountError:
                print (CountError)

            self.Replace()

        else:
            CountError = self.FileVerify()

            print('Static configuration :', self.Wan, "-"*3, self.Host)

            if CountError:
                print (CountError)

        return CountError

excel = pd.read_csv(os.path.join(os.getcwd(),'FortiConfig','Basic.csv'),usecols=['Host','WAN','LAN','Gateway'])

for i in range(len(excel)):
    FortiGen((excel['Host'][i]),(excel['WAN'][i]),(excel['LAN'][i]),(excel['Gateway'][i]))
    
    FortiGen.Main(FortiGen.Sort[i])
    
