Function ConfigUpdate
{

    [CmdletBinding()] 
    Param
        (
            [Parameter(Mandatory=$false)][string]$ToolDir="C:\Tools\FortiConfig",
            [Parameter(Mandatory=$false)][string]$StaticConfigurationPath = "$ToolDir\Static.txt",
            [Parameter(Mandatory=$false)][string]$DHCPConfigurationPath = "$ToolDir\DHCP.txt",
            [Parameter(Mandatory=$false)][string]$ServerName = "WLCK01.otcf.pl",
            [Parameter(Mandatory=$false)][string]$UpdatePath = "\\$ServerName\IT\Administracja\FortiGateConfig",
            [Parameter(Mandatory=$false)][string]$FortiGateConfigFile = "FortiGateConfigFile"
        )

    Function ConnectivityChecker

    {
        $ServerPing = Test-NetConnection -ComputerName $ServerName -ErrorAction SilentlyContinue
        $ServerSMB = Test-NetConnection -ComputerName $ServerName -Port 445 -ErrorAction SilentlyContinue

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
                                    Write-Host "`nMissing update file/s :" -ForegroundColor Red
                                    Write-Host "`nStatic File : "$RemoteStaticConfigExist -ForegroundColor Yellow
                                    Write-Host "DHCP File : $RemoteDHCPConfigExist" -ForegroundColor Yellow
                                    Write-Host "General Connectivity Status : $ConnectivityVerdict" -ForegroundColor Yellow
                                    }
                            }
                    }
                ELSE 
                    {
                        Write-Host "`nConnection problem occurred`n"
                        $ServiceStatus
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

                Copy-Item  "$UpdatePath\Static.txt" -Destination $ToolDir -Force -Confirm 
                Copy-Item  "$UpdatePath\DHCP.txt" -Destination $ToolDir -Force -Confirm

            }
        Catch 
            {
                    #ErrorCatch Function
            }

            $VerifyUpdateDHCP = Get-FileHash $DHCPConfigurationPath -ErrorAction SilentlyContinue
            $VerifyUpdateStatic = Get-FileHash $StaticConfigurationPath -ErrorAction SilentlyContinue

            $RemoteStaticHash = Get-FileHash "$UpdatePath\Static.txt" -ErrorAction SilentlyContinue
            $RemoteDHCPHash = Get-FileHash "$UpdatePath\DHCP.txt" -ErrorAction SilentlyContinue

            IF (($VerifyUpdateDHCP.Hash -EQ $RemoteDHCPHash.Hash) -and ($VerifyUpdateStatic.Hash -EQ $RemoteStaticHash.Hash))
                {Write-Host "Update Succeed"}
            ELSE {Write-Host "Something went wrong"}    

    }

    Function UserChoice

    {
        
        $IsOKOrNot = UpdateFileVerify
        IF ("OK" -EQ $IsOKOrNot)
            {
                Write-host "`nUpdate pending, do you want to proceed? :" -ForegroundColor Green

                $UserChoice = "No"
                $UserChoice = Read-Host "Y to Continue, Other Key to Stop"

                Switch ($UserChoice)
                
                {
                    Y { $UpdateChoice = 1 }
                    Ye { $UpdateChoice = 1 }
                    Yes { $UpdateChoice = 1 }
                    Default { $UpdateChoice = 0 }
                }

                IF ($UpdateChoice -EQ 1)
                
                    {
                        Try {FinallyJustUpdate}
                        Catch {<#Error#>}
                    }
            }

    }

    UserChoice
}

#Export-ModuleMember UserChoice

ConfigUpdate