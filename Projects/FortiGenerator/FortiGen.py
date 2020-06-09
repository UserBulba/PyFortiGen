import os
import sys
import pandas as pd
import datetime
import functools

class FortiGen():

    Sort = []

    def __init__(self, Host, Wan, Lan, Gateway, DHCPStart=2, DHCPEnd=100, Override=True):
        self.Host = Host
        self.Wan = Wan
        self.Lan = Lan
        self.DHCPStart = DHCPStart
        self.DHCPEnd = DHCPEnd
        self.Gateway = Gateway
        self.TimeZone = '29'
        self.overrideMode = Override
        self.Path = os.getcwd()
        self.Sys = os.path.join(self.Path, self.Host)

        FortiGen.Sort.append(self)

    def __repr__(self):
        return ('HOST - {}, WAN - {}, LAN - {}, Gateway - {} '.format(self.Host,self.Wan,self.Lan,self.Gateway))

    def Wrapper_logFilePath(self):
        #Log changes to log file.
        #Wrapping function to logfile
        def Wrapper(func):
            def func_with_wrapper(*args,**kwargs):
                file = open(self,'a')
                file.write('-'*20 + '\n')
                file.write('Function "{}" started at {}\n'.format(str(func.__name__),datetime.datetime.now().isoformat()))
                file.write('Following arguments were used:\n')
                file.write(' '.join('{}'.format(x) for x in args))
                file.write('\n')
                file.write(' '.join('{}={}'.format(k,v) for (k,v) in kwargs.items()))
                file.write('\n')
                result = (str(*args),str(**kwargs))
                #file.write('Function returned {}\n'.format(result))
                file.close()
                return result
            return func_with_wrapper
        return Wrapper

    def FileVerify(self):
        #Try to create catalogue for configuration if error, return error to main loop for skip.
        Error = 0
        try:
            #Validaton of paths
            if not os.path.exists(os.path.join(self.Path, self.Host)):
                os.makedirs(os.path.join(self.Path, self.Host))
            else:
                #Count errors, to continue in loop or override if enabled.
                if not self.overrideMode:
                    Error =+ 1

                print ("Catalogue for device {Type}".format(Type = "found" if not self.overrideMode else "overridden"))

        except:
            print ("Sorry, error occurred :",sys.exc_info()[0])
            #Count errors, to continue in loop
            Error =+ 1

        return Error

    @Wrapper_logFilePath(os.path.join(os.getcwd(),'changelog.txt'))
    def Replace(self):

        Subnet = self.Lan.split(' ')
        LanIP = (Subnet[0]).split('.')

        DHCPStartAddress = (LanIP[0] + '.'+ LanIP[1] + '.' + LanIP[2] + '.' + str(self.DHCPStart))
        DHCPEndAddress = (LanIP[0] + '.'+ LanIP[1] + '.' + LanIP[2] + '.' + str(self.DHCPEnd))

        with open(os.path.join(self.Path,'FortiConfig','DHCP.txt')) as Config:
            newText = Config.read().replace('FW502R5618001244', self.Host)
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

    #@Wrapper_logFilePath(os.getcwd()+'changelog.txt')
    def Main(self):
        if self.Wan == 'DHCP':
            print ('DHCP configuration :', self.Wan, "-"*3, self.Host)
            self.Replace()

        else:
            print('Static configuration :', self.Wan, "-"*3, self.Host)

        return

#Txt/Csv ?
excel = pd.read_csv(os.path.join(os.getcwd(),'FortiConfig','Basic.csv'),usecols=['Host','WAN','LAN','Gateway'])

for i in range(len(excel)):
    FortiGen((excel['Host'][i]),(excel['WAN'][i]),(excel['LAN'][i]),(excel['Gateway'][i]))

    #Skip position in error occured.
    if FortiGen.FileVerify(FortiGen.Sort[i]) == 1:
        continue
    else :
        FortiGen.Main(FortiGen.Sort[i])

