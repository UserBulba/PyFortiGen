$Path = "C:\Users\piokmi\Desktop\FortiConfig\CI4.csv"

$Config = Import-Csv $Path

Foreach($Value in $Config)

{
    
    $FortiHost = $Value.Host
    $FortiLAN = $Value.LAN
    $FortiWAN = $Value.WAN
    $FortiStaticGateway = $Value.Gateway
    $FortiDHCP_Start = $Value.DHCP_Start
    $FortiDHCP_End = $Value.DHCP_End

    $Split_IP,$Split_Mask = $FortiLAN.split(' ')

    $Path = ""
    $Path = "C:\Users\piokmi\Desktop\FortiConfig\Done\$FortiHost\fgt_system.conf"
    New-Item -ItemType directory -Path "C:\Users\piokmi\Desktop\FortiConfig\Done\$FortiHost"


    IF ("DHCP" -NotLike $Value.WAN)

    {

        #Zmiana Hostname oraz Alias.
        ((Get-Content -path "C:\Users\piokmi\Desktop\FortiConfig\Static.txt") -replace 'FW502R5618001244',$FortiHost) | Set-Content -Path $Path

        #Zmiana adresacji LAN
        $ReplaceLAN =  "set ip" + " " + $FortiLAN
        ((Get-Content -path $Path) -replace 'set ip 10.10.20.1 255.255.255.0',$ReplaceLAN) | Set-Content -Path $Path

        #Zmiana LAN DHCP Gateway
        $ReplaceDHCP_GW =  "set default-gateway" + " " + $Split_IP
        ((Get-Content -path $Path) -replace 'set default-gateway 10.10.20.1',$ReplaceDHCP_GW) | Set-Content -Path $Path

        #Zmiana LAN DHCP Start
        $ReplaceDHCP_Start =  "set start-ip" + " " + $FortiDHCP_Start
        ((Get-Content -path $Path) -replace 'set start-ip 10.10.20.2',$ReplaceDHCP_Start) | Set-Content -Path $Path

        #Zmiana LAN DHCP End
        $ReplaceDHCP_End =  "set end-ip" + " " + $FortiDHCP_End
        ((Get-Content -path $Path) -replace 'set end-ip 10.10.20.254',$ReplaceDHCP_End) | Set-Content -Path $Path

        #Zmiana adresu WAN
        $ReplaceWAN =  "set ip" + " " + $FortiWAN
        ((Get-Content -path $Path) -replace 'set ip 91.226.50.102 255.255.248.0',$ReplaceWan) | Set-Content -Path $Path
        
        #Zmiana static routingu
        $ReplaceStatic = "set gateway" + " " + $FortiStaticGateway
        ((Get-Content -path $Path) -replace 'set gateway 91.226.50.97',$ReplaceStatic) | Set-Content -Path $Path

    }

    ELSE 

    {

        #Zmiana Hostname oraz Alias.
        ((Get-Content -path "C:\Users\piokmi\Desktop\FortiConfig\DHCP.txt") -replace 'FW502R5618001244',$FortiHost) | Set-Content -Path $Path

        #Zmiana adresacji LAN
        $ReplaceLAN =  "set ip" + " " + $FortiLAN
        ((Get-Content -path $Path) -replace 'set ip 10.10.20.1 255.255.255.0',$ReplaceLAN) | Set-Content -Path $Path
        
        #Zmiana LAN DHCP Gateway
        $ReplaceDHCP_GW =  "set default-gateway" + " " + $Split_IP
        ((Get-Content -path $Path) -replace 'set default-gateway 10.10.20.1',$ReplaceDHCP_GW) | Set-Content -Path $Path
        
        #Zmiana LAN DHCP Start
        $ReplaceDHCP_Start =  "set start-ip" + " " + $FortiDHCP_Start
        ((Get-Content -path $Path) -replace 'set start-ip 10.10.20.2',$ReplaceDHCP_Start) | Set-Content -Path $Path
        
        #Zmiana LAN DHCP End
        $ReplaceDHCP_End =  "set end-ip" + " " + $FortiDHCP_End
        ((Get-Content -path $Path) -replace 'set end-ip 10.10.20.254',$ReplaceDHCP_End) | Set-Content -Path $Path

    }

}
