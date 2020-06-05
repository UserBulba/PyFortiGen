import os
import pandas as pd

path = os.getcwd()


class FortiGen():
    
    sort = []
    
    def __init__(self,host,wan,lan,gateway):
        self.host = host
        self.wan = wan
        self.lan = lan
        self.gateway = gateway
        FortiGen.sort.append(self)
        self.timezone = '29'

        
    def Show(self):
        print('Host:    {}\n'.format(self.host).upper())
        print('Wan:     {}'.format(self.wan))
        print('Lan:     {}'.format(self.lan))
        print('Gateway: {}'.format(self.gateway))
        print(FortiGen.sort)
        return 



    def CreateHostName(self):
        try:
            os.makedirs(os.path.join(path,self.host))
        except:
            pass
        sys = os.path.join(path,self.host)
        splitIP = self.lan.split(' ')
        ip_v3 = (splitIP[0]).split('.')
        dhcp_start = (ip_v3[0] + '.'+ip_v3[1] + '.'+ip_v3[2] + '.2')
        dhcp_end = (ip_v3[0] + '.'+ip_v3[1] + '.'+ip_v3[2] + '.100')

        with open(os.path.join(path,'FortiConfig','DHCP.txt')) as f:
            newText=f.read().replace('FW502R5618001244',self.host).replace('set timezone 04','set timezone '+self.timezone).replace('set ip 10.10.20.1 255.255.255.0','set ip '+self.lan).replace('set default-gateway 10.10.20.1','set default-gateway ' + splitIP[0]).replace('set start-ip 10.10.20.2','set start-ip '+dhcp_start).replace('set end-ip 10.10.20.254','set end-ip ' + dhcp_end).replace('set ip 91.226.50.102 255.255.248.0', 'set ip '+ self.wan).replace('set gateway 91.226.50.97', 'set gateway ' + self.gateway)


        with open(os.path.join(sys,'fgt_config.conf'), "w") as f:
            f.write(newText)       
        return


    def modeValidation(self):
        print(self.host)
        if self.wan == 'DHCP':
            self.CreateHostName()
        else:
            print('No File')
        
        return  


excel = pd.read_csv(os.path.join(path,'FortiConfig','Basic.csv'),usecols=['Host','WAN','LAN','Gateway'])


s = 0
for i in range(len(excel)):
    FortiGen((excel['Host'][i]),(excel['WAN'][i]),(excel['LAN'][i]),(excel['Gateway'][i]))
    
    FortiGen.modeValidation(FortiGen.sort[i])
    
    

'''
        dhcp_txt = open(os.path.join(path,'FortiConfig','DHCP.txt'),'rt')

        os.makedirs(os.path.join(path,self.host))
        sys = os.path.join(path,self.host)
        dhcp_output = open(os.path.join(sys,'fgt_config.conf'),'w+')



        for line in dhcp_txt:
           dhcp_output.write(line.replace('FW502R5618001244',self.host))
        

        dhcp_output.close()
        dhcp_txt.close()
'''
        

    






#for p in FortiGen.sort:
#    FortiGen.Show(p)

'''
my_list = []

for i in range((excel.shape[0])):
    my_list.append(list(excel.iloc[i, :]))

print(my_list[0][0])
s = 0
for p in my_list:
    FortiGen((my_list[s][s]),(my_list[s][s+1]),(my_list[s][s+2]),(my_list[s][s+3]))

for t in FortiGen.sort:
    FortiGen.Show(t)
'''