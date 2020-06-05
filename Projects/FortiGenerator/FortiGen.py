import os
import pandas as pd


class FortiGen():
    
    def __init__(host,wan,lan,gateway):
        self.host = host
        self.wan = wan
        self.lan = lan
        self.gateway = gateway

    
    def modeValidation(self):

        if self.wan == 'DHCP':
            
