<#
 .Description
  FortiConfig Generator.

 .Example
   FortiConfig -Folder Done_v10 -CsvName Source_v4 -LinkMonitorIP 1.2.3.4

 .Example
   FortiConfig -Folder Done_v10 -CsvName Source_v4 -LinkMonitor NO

  .Notes
   # -Folder Catalogue in C:\Tools\FortiConfig
   # -CsvName Source csv File ine C:\Tools\FortiConfig
   # -LinkMonitorIP 1.2.3.4
   # -LinkMonitor NO (Optional)
   # -TimeZone 29
   # 0

 .Notes
   # V 0.1 - 1 Release.
 .Notes
   # V 0.2 - Added Link Monitor.
 .Notes
   # V 0.3 - TimeZone.
 .Notes
   # V 0.4 - Config Update.
 .Notes
   # V 0.5 - Up/Down.
#>
Function FortiConfig

{

    [CmdletBinding(DefaultParameterSetName="Do")]
    Param
        (
        [Parameter(Mandatory=$false)][string]$ToolDir="C:\Tools\FortiConfig",
        [Parameter(ParameterSetName="Update",Mandatory=$false,HelpMessage="Update config files : Yes/No")][ValidateSet("Yes","No")][string]$Update,
        [Parameter(ParameterSetName="Do",Mandatory=$false)][string]$LinkMonitor="Enable",
        [Parameter(ParameterSetName="Do",Mandatory=$false)][ipaddress]$LinkMonitorIP='10.70.8.90',
        [Parameter(ParameterSetName="Do",Mandatory=$false)][string]$ChangeDirectory="C:\tmp",
        [Parameter(ParameterSetName="Do",Mandatory=$false)][string]$ChangeLog="Config.Log",
        [Parameter(ParameterSetName="Do",Mandatory=$false)][string]$TimeZone=29,
        [Parameter(ParameterSetName="Do",Mandatory=$false)][string]$StartDHCP_Range='2',
        [Parameter(ParameterSetName="Do",Mandatory=$false)][string]$EndDHCP_Range='100',
        [Parameter(ParameterSetName="Do",Mandatory=$true,HelpMessage="Config destination folder name",Position=1)][string]$Folder,
        [Parameter(ParameterSetName="Do",Mandatory=$true,HelpMessage="Csv config file name ",Position=2)][string]$CsvName
        )

    Function FortiGenerator
    {

        [CmdletBinding()]
        Param
            (
                [Parameter(Mandatory=$false)][int]$FortiUpstreamBandwidth,
                [Parameter(Mandatory=$false)][int]$FortiDownstreamBandwidth
            )

            IF ((Test-Path -Path $ChangeDirectory -PathType container) -ne $True)

                {
                    New-Item $ChangeDirectory -Type directory
                }

            $ChangePath = $ChangeDirectory + "\" + $ChangeLog

            IF ((Test-Path -Path $ToolDir -PathType container) -ne $True)

                {
                    New-Item $ToolDir -Type directory
                }

            $FolderToolDir = "$ToolDir\$Folder"

            IF ((Test-Path -Path $FolderToolDir -PathType container) -ne $True)

                {
                    New-Item $FolderToolDir -Type directory
                }

            "---" | Out-File $ChangePath -Append

            $Path="$ToolDir\$CsvName"

            IF ($Path.Contains(".csv")){}
            ELSE

                {$New = $Path + ".csv"
                $Path = $New}

            $Config = Import-Csv $Path

        Foreach($Value in $Config)

        {

            $FortiHost = $Value.Host
            $FortiLAN = $Value.LAN
            $FortiWAN = $Value.WAN
            $FortiStaticGateway = $Value.Gateway
            $FortiUpstreamBandwidth = $Value.UP
            $FortiDownstreamBandwidth = $Value.Down

            $Split_IP,$Split_Mask = $FortiLAN.split(' ')
            $Split_IP_1,$Split_IP_2,$Split_IP_3,$Split_IP_4 = $Split_IP.split('.')
            $FortiAddress = $Split_IP_1 + "." + $Split_IP_2 + "." + $Split_IP_3 + "."
            $FortiDHCP_Start = $FortiAddress + $StartDHCP_Range
            $FortiDHCP_End = $FortiAddress  + $EndDHCP_Range

            $Path = "$FolderToolDir\$FortiHost\fgt_system.conf"

            IF (("" -eq $Value.WAN) -and ("" -eq $Value.Gateway))
            {
                Write-Host "$FortiHost : Wan and Gateway are blank in device" -ForegroundColor Red
                Continue
            }

            New-Item -ItemType directory -Path "$FolderToolDir\$FortiHost" -ErrorAction SilentlyContinue | Out-Null

            IF (("DHCP" -Like $Value.Gateway) -or ("DHCP" -Like $Value.WAN))
            {
                $Value.Host | Out-File $ChangePath -Append


                #Zmiana Hostname oraz Alias
                ((Get-Content -path "$ToolDir\DHCP.txt") -replace 'FW502R5618001244',$FortiHost) | Set-Content -Path $Path

                #Zmiana Strefy czasowej
                $ReplaceTimeZone = "set timezone" + " " + $TimeZone
                ((Get-Content -path $Path) -replace 'set timezone 04',$ReplaceTimeZone) | Set-Content -Path $Path

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

                IF ($LinkMonitor -ne "NO")
                {
                    #Link Monitor
                    $ValEdit = '"IPSecUP"'
                    $Val2IPSer = $LinkMonitorIP
                    $Val3IPSou = $Split_IP
                    $Val = "config system link-monitor`n    edit " + $ValEdit
                    $Val2 = "`n        set server " + $Val2IPSer
                    $Val3 = "`n        set source-ip " + $Val3IPSou
                    $Val4 = "`n        set interval 60"
                    $Val5 = "`n        set update-cascade-interface disable"
                    $Val6 = "`n        set update-static-route disable"
                    $Val7 = "`n    next"
                    $Val8 = "`nend"

                    $ValALL = $Val + $Val2 + $Val3 + $Val4 + $Val5 + $Val6 + $Val7 + $Val8
                    Add-Content -Path $Path -Value $ValALL
                }

                IF ($FortiUpstreamBandwidth -and $FortiDownstreamBandwidth)
                {
                    #Bandwidth
                    $Content = Get-Content -Path $Path

                    $Match = "set mode dhcp"
                    $Line = Select-String -Pattern $Match -Path $Path | Select-Object -First 1
                    $Index = $Line.LineNumber + 3

                    $ValBan1 = "        set estimated-upstream-bandwidth " + $FortiUpstreamBandwidth
                    $ValBan2 = "`n        set estimated-downstream-bandwidth " + $FortiDownstreamBandwidth

                    $NewLine = $ValBan1 + $ValBan2

                    $NewContent = @()
                    0..($Content.Count-1) | Foreach-Object {
                        if ($_ -eq $index) {
                            $NewContent += $NewLine
                        }
                        $NewContent += $Content[$_]
                    }

                    $NewContent | Out-File -FilePath $Path -Force -Encoding utf8
                }

                Write-Host "$FortiHost : DHCP Configuration done" -ForegroundColor Green
            }

            ELSE
            {
                $Value.Host | Out-File $ChangePath -Append

                #Zmiana Hostname oraz Alias.
                ((Get-Content -path "$ToolDir\Static.txt") -replace 'FW502R5618001244',$FortiHost) | Set-Content -Path $Path

                #Zmiana Strefy czasowej
                $ReplaceTimeZone = "set timezone" + " " + $TimeZone
                ((Get-Content -path $Path) -replace 'set timezone 04',$ReplaceTimeZone) | Set-Content -Path $Path

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

                IF ($LinkMonitor -ne "NO")
                {
                    #Link Monitor
                    $ValEdit = '"IPSecUP"'
                    $Val2IPSer = $LinkMonitorIP
                    $Val3IPSou = $Split_IP
                    $Val = "config system link-monitor`n    edit " + $ValEdit
                    $Val2 = "`n        set server " + $Val2IPSer
                    $Val3 = "`n        set source-ip " + $Val3IPSou
                    $Val4 = "`n        set interval 60"
                    $Val5 = "`n        set update-cascade-interface disable"
                    $Val6 = "`n        set update-static-route disable"
                    $Val7 = "`n    next"
                    $Val8 = "`nend"

                    $ValALL = $Val + $Val2 + $Val3 + $Val4 + $Val5 + $Val6 + $Val7 + $Val8
                    Add-Content -Path $Path -Value $ValALL
                }

                IF ($FortiUpstreamBandwidth -and $FortiDownstreamBandwidth)
                {
                    #Bandwidth
                    $Content = Get-Content -Path $Path

                    $Match = $ReplaceWAN
                    $Line = Select-String -Pattern $Match -Path $Path
                    $Index = $Line.LineNumber + 3

                    $ValBan1 = "        set estimated-upstream-bandwidth " + $FortiUpstreamBandwidth
                    $ValBan2 = "`n        set estimated-downstream-bandwidth " + $FortiDownstreamBandwidth

                    $NewLine = $ValBan1 + $ValBan2

                    $NewContent = @()
                    0..($Content.Count-1) | Foreach-Object {
                        if ($_ -eq $index) {
                            $NewContent += $NewLine
                        }
                        $NewContent += $Content[$_]
                    }

                    $NewContent | Out-File -FilePath $Path -Force -Encoding utf8
                }

                Write-Host "$FortiHost : Static Configuration done - WAN Info : $FortiWan - WAN GW : $FortiStaticGateway" -ForegroundColor Green
            }

        }

    }

    Function ConfigUpdate
    {

        [CmdletBinding()]
        Param
            (
                [Parameter(Mandatory=$false)][string]$StaticConfigurationPath = "$ToolDir\Static.txt",
                [Parameter(Mandatory=$false)][string]$DHCPConfigurationPath = "$ToolDir\DHCP.txt",
                [Parameter(Mandatory=$false)][string]$ServerName = "WLCK01.otcf.pl",
                [Parameter(Mandatory=$false)][string]$UpdatePath = "\\$ServerName\IT\Administracja\FortiGateConfig",
                [Parameter(Mandatory=$false)][string]$FortiGateConfigFile = "FortiGateConfigFile"
            )

        Function ConnectivityChecker

        {
            $ServerPing = Test-NetConnection -ComputerName $ServerName -ErrorAction SilentlyContinue -WarningAction SilentlyContinue
            $ServerSMB = Test-NetConnection -ComputerName $ServerName -Port 445 -ErrorAction SilentlyContinue -WarningAction SilentlyContinue

            $ServerPing_Status = $ServerPing.PingSucceeded
            $ServerSMB_Status = $ServerSMB.TcpTestSucceeded

            $ServiceStatus = @{}
            $ServiceStatus.Add('PING',$ServerPing_Status)
            $ServiceStatus.Add('SMB',$ServerSMB_Status)

            $OK = 0
            ForEach ($Key IN $ServiceStatus.Keys)
                {
                    IF ($ServiceStatus[$Key] -eq "True")
                    {$OK++}
                }

                IF ($OK -eq $ServiceStatus.Count)
                    {
                        $ConnectivityStatus = "OK"
                    }
                ELSE
                    {
                        $ConnectivityStatus = "Failed"
                    }

            Return $ConnectivityStatus
        }

        Function UpdateVerify

        {
            Try
                {
                    $ConnectivityVerdict = ConnectivityChecker
                    IF ("OK" -EQ $ConnectivityVerdict)
                        {
                            $PathConnectivity = Test-Path -Path $UpdatePath -ErrorAction SilentlyContinue
                            IF ($PathConnectivity)
                                {
                                    $RemoteStaticConfigExist = Test-Path "$UpdatePath\Static.txt" -ErrorAction SilentlyContinue
                                    $RemoteDHCPConfigExist = Test-Path "$UpdatePath\DHCP.txt"  -ErrorAction SilentlyContinue

                                    IF ($RemoteStaticConfigExist -and $RemoteDHCPConfigExist)
                                        {$UpdatePossible = "OK"}
                                    ELSE
                                        {
                                        IF (!$RemoteStaticConfigExist) {$StatiColor = "Red"}
                                        ELSE {$StatiColor = "Green"}

                                        IF (!$RemoteDHCPConfigExist) {$DHCPColor = "Red"}
                                        ELSE {$DHCPColor = "Green"}

                                        Write-Host "`nMissing update files :" -ForegroundColor Red
                                        Write-Host "Please check the files path : $UpdatePath" -ForegroundColor Yellow
                                        Write-Host "`nStatic.txt - File : $RemoteStaticConfigExist" -ForegroundColor $StatiColor
                                        Write-Host "DHCP.txt - File : $RemoteDHCPConfigExist" -ForegroundColor $DHCPColor
                                        Write-Host "`nGeneral Connectivity Status : $ConnectivityVerdict" -ForegroundColor Green
                                        }
                                }
                        }
                    ELSE
                        {
                            Write-Host "`nConnection problem occurred!" -ForegroundColor Red
                            Write-Host "Connection to host : $ServerName - unavailable"  -ForegroundColor Red
                        }
                }

            Catch
                {
                    #ErrorCatch Function
                }

            Return $UpdatePossible
        }

        Function UpdateFileVerify

        {

            $StartFileVerify = UpdateVerify
            IF ("OK" -EQ $StartFileVerify)

            {

                $LocalStaticConfigExist = Test-Path $StaticConfigurationPath -ErrorAction SilentlyContinue
                $LocalDHCPConfigExist = Test-Path $DHCPConfigurationPath -ErrorAction SilentlyContinue

                IF ($LocalStaticConfigExist -and $LocalDHCPConfigExist)

                {
                    $LocalStaticHash = Get-FileHash $StaticConfigurationPath -ErrorAction SilentlyContinue
                    $LocalDHCPHash = Get-FileHash $DHCPConfigurationPath -ErrorAction SilentlyContinue

                    $LocalStaticInfo = Get-Item $StaticConfigurationPath -ErrorAction SilentlyContinue
                    $LocalDHCPInfo = Get-Item $DHCPConfigurationPath -ErrorAction SilentlyContinue
                }

                ELSE {$JustUpdateItNow = "OK"}

                $RemoteStaticHash = Get-FileHash "$UpdatePath\Static.txt" -ErrorAction SilentlyContinue
                $RemoteDHCPHash = Get-FileHash "$UpdatePath\DHCP.txt" -ErrorAction SilentlyContinue

                $RemoteStaticInfo = Get-Item "$UpdatePath\Static.txt" -ErrorAction SilentlyContinue
                $RemoteDHCPInfo = Get-Item "$UpdatePath\DHCP.txt" -ErrorAction SilentlyContinue

                IF ("OK" -NE $JustUpdateItNow)
                {
                    $UpdateInfoStatus = @{}

                    IF ($RemoteStaticHash.Hash -EQ $LocalStaticHash.Hash)
                        {$StaticHash = "Failed"}
                    ELSE {$StaticHash = "OK"}

                    $UpdateInfoStatus.Add('StaticHash',$StaticHash)

                    IF ($RemoteDHCPHash.Hash -EQ $LocalDHCPHash.Hash)
                        {$DHCPHash = "Failed"}
                    ELSE {$DHCPHash = "OK"}

                    $UpdateInfoStatus.Add('DHCPHash',$DHCPHash)

                    IF ($RemoteStaticInfo.CreationTime -GT $LocalStaticInfo.CreationTime)
                        {$StaticCreationTime = "OK"}
                    ELSE {$StaticCreationTime = "Failed"}

                    $UpdateInfoStatus.Add('StaticInfoTime',$StaticCreationTime)

                    IF ($RemoteDHCPInfo.CreationTime -GT $LocalDHCPInfo.CreationTime)
                        {$DHCPCreationTime = "OK"}
                    ELSE {$DHCPCreationTime = "Failed"}

                    $UpdateInfoStatus.Add('DHCPInfoTime',$DHCPCreationTime)

                    $OK = 0
                    ForEach ($Key IN $UpdateInfoStatus.Keys)
                        {
                            IF ($UpdateInfoStatus[$Key] -eq "OK")
                            {$OK++}
                        }

                    IF ($OK -eq $UpdateInfoStatus.Count)
                        {
                            $TimeToUpgrade = "OK"
                        }
                        ELSE
                        {
                            $TimeToUpgrade = "Failed"

                        }
                }
                ELSE
                {
                    $TimeToUpgrade = "OK"
                }

            Return $TimeToUpgrade

            }



        }

        Function FinallyJustUpdate

        {
            Try
                {
                    $FortiGateConfigPath = Join-Path -Path $ToolDir -ChildPath $FortiGateConfigFile

                    IF ((Test-Path -Path $FortiGateConfigPath -PathType container) -ne $True)
                    {
                        New-Item $FortiGateConfigPath -Type directory -Force
                        IF ((Test-Path -Path $FortiGateConfigPath -PathType container) -eq $True)
                        {
                            $MakeThemNinja = Get-Item $FortiGateConfigPath -Force
                            $MakeThemNinja.Attributes = "Hidden"
                        }

                        Copy-Item "$ToolDir\Static.txt" -Destination $FortiGateConfigPath -Force -ErrorAction SilentlyContinue
                        Copy-Item "$ToolDir\DHCP.txt" -Destination $FortiGateConfigPath -Force -ErrorAction SilentlyContinue
                    }

                    ELSE
                    {
                        IF ((Test-Path -Path $FortiGateConfigPath -PathType container) -eq $True)
                        {
                            $MakeThemNinja = Get-Item $FortiGateConfigPath -Force
                            $MakeThemNinja.Attributes = "Hidden"
                        }

                        Copy-Item "$ToolDir\Static.txt" -Destination $FortiGateConfigPath -Force -ErrorAction SilentlyContinue
                        Copy-Item "$ToolDir\DHCP.txt" -Destination $FortiGateConfigPath -Force -ErrorAction SilentlyContinue
                    }

                    Copy-Item  "$UpdatePath\Static.txt" -Destination $ToolDir -Force #-Confirm
                    Copy-Item  "$UpdatePath\DHCP.txt" -Destination $ToolDir -Force #-Confirm

                }

            Catch

                {
                    Write-Error "Update Problem Occure"
                }

                $VerifyUpdateDHCP = Get-FileHash $DHCPConfigurationPath -ErrorAction SilentlyContinue
                $VerifyUpdateStatic = Get-FileHash $StaticConfigurationPath -ErrorAction SilentlyContinue

                $RemoteStaticHash = Get-FileHash "$UpdatePath\Static.txt" -ErrorAction SilentlyContinue
                $RemoteDHCPHash = Get-FileHash "$UpdatePath\DHCP.txt" -ErrorAction SilentlyContinue

                IF (($VerifyUpdateDHCP.Hash -EQ $RemoteDHCPHash.Hash) -and ($VerifyUpdateStatic.Hash -EQ $RemoteStaticHash.Hash))
                    {Write-Host "`nUpdate Succeed" -ForegroundColor Green}
                ELSE {Write-Host "`nSomething went wrong" -ForegroundColor Red}

        }

        Function UserChoice

        {

            [CmdletBinding()]
            Param
                ([Parameter(Mandatory=$false,HelpMessage="Yes/No")][ValidateSet("Yes","No")][string]$UpdateChoice = "No")

            $IsOKOrNot = UpdateFileVerify
            IF ("OK" -EQ $IsOKOrNot)
                {

                    Write-host "`nUpdate pending, do you want to proceed? :" -ForegroundColor Green

                    $UpdateChoice = Read-Host "Yes to Continue, No to Stop "

                    IF ($UpdateChoice -EQ "Yes")

                        {
                            Try {FinallyJustUpdate}
                            Catch {Write-Error "Update Problem Occure"}

                        }
                }

        }

        UserChoice
    }

    IF ($Update)
    {ConfigUpdate}

    ELSE
    {FortiGenerator}

}

Export-ModuleMember -Function FortiConfig