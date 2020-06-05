<# 
 .Description
  FortiObjGenerator 

 .Example
  FortiObjGenerator -CsvName Source_Addr -Folder Done10

#>

Function FortiObjGenerator

{

    [CmdletBinding()] 
    Param
        (
        [Parameter(Mandatory=$true,HelpMessage="Config destination folder name",Position=1)][string]$Folder,
        [Parameter(Mandatory=$true,HelpMessage="Csv config file name ",Position=2)][string]$CsvName,
        [Parameter(Mandatory=$false)][string]$ChangePath="C:\tmp\Config.Log",
        [Parameter(Mandatory=$false)][string]$ToolDir="C:\Tools\FortiConfig",
        [Parameter(Mandatory=$false)][string]$GroupEnable="Enable",
        [Parameter(Mandatory=$false)][string]$GroupName="S4B"
        )

        $ObjNames = @{}

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

    IF ((Test-Path -Path $Path) -eq $True)

    {

        $Config = Import-Csv $Path            

        $Path = "$FolderToolDir\FgObj.conf"

        IF ((Test-Path -Path $FolderToolDir) -eq $True)

                {
                    Remove-Item $Path -Confirm -ErrorAction SilentlyContinue
                }

            Add-Content -Path $Path -Value "config firewall address"

            Foreach($Value in $Config)

            {

                $IP = $Value.Host
                $Split_IP,$Split_Mask = $IP.Split("/")
                $Name = "Microsoft_" + $GroupName + "_" + $Split_IP
                $ObjNames.Add($Name, $GroupName)

                        $Val =  "    edit " + $Name
                        $Val1 = "`n        set subnet " + $IP
                        $Val2 = "`n    next"


                        $ValALL = $Val + $Val1 + $Val2
                        Add-Content -Path $Path -Value $ValALL
                    
            }

        Add-Content -Path $Path -Value "end"

        IF ($LinkMonitor -ne "NO")

        {

            ForEach ($S4B in $ObjNames.Keys)
                {
                    $S4BObj = $S4B + " "
                    $GrpMem = $GrpMem + $S4BObj
                }
            
            Add-Content -Path $Path -Value "`nconfig firewall addrgrp"

            $Val =  "    edit " + $GroupName
            $Val1 = "`n        set member " + $GrpMem
            $Val2 = "`n    next"
            $Val3 = "`nend"

            $ValALL = $Val + $Val1 + $Val2 + $Val3
            Add-Content -Path $Path -Value $ValALL

            Write-Host "`nGroup Members :`n" -ForegroundColor Green
            Write-Host $GrpMem

        }
    }
}

Export-ModuleMember -Function FortiObjGenerator

# SIG # Begin signature block
# MIIH8AYJKoZIhvcNAQcCoIIH4TCCB90CAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUBZPFJzCYnAtLiXFWVVi6uStX
# heWgggVkMIIFYDCCBEigAwIBAgITcwAAA+lrKsgqUZtfwwAAAAAD6TANBgkqhkiG
# 9w0BAQsFADA+MRIwEAYKCZImiZPyLGQBGRYCcGwxFDASBgoJkiaJk/IsZAEZFgRv
# dGNmMRIwEAYDVQQDEwlPVENGU0EtQ0EwHhcNMTkwMTIyMjAxNTIwWhcNMjAwMTIy
# MjAxNTIwWjBWMRIwEAYKCZImiZPyLGQBGRYCcGwxFDASBgoJkiaJk/IsZAEZFgRv
# dGNmMQ4wDAYDVQQDEwVVc2VyczEaMBgGA1UEAxMRUGlvdHIgS21pZWNpayBBRE0w
# ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCmlmG5zaf8uKlPt8rgvjwl
# aJ1cuwV2fFU9Qb94j/nZYF6eey8IqoCfgBGUykeyUVdFT3O6cXXsxuryIB8Nq5eL
# FCNZDVLdgKZmjD9QocZ7T5xGIJXPXhLJzYwFMkkQeTTSwE1f7MP4i2rHxBAm5smW
# aPSqN84gQLAb6woIcpzoY3VqXhKcK9n6s/OhbX81ngltsHRg6H0E6DS3febBBhH6
# GNCwC2g4EdZoXcRT8Ngo56tn/o9LyfrgPRceQhP0iPhU53ZkfgQFVWAgkRBXQiC9
# N4b4nuuC/RK797JPjGh7qBe1W8gZvlhKSOyBIRmWStqnerovQ+xFBWuEjd3PF7NB
# AgMBAAGjggI9MIICOTAlBgkrBgEEAYI3FAIEGB4WAEMAbwBkAGUAUwBpAGcAbgBp
# AG4AZzATBgNVHSUEDDAKBggrBgEFBQcDAzAOBgNVHQ8BAf8EBAMCB4AwHQYDVR0O
# BBYEFDHzHmh6qwmuWS6UTKP9armToRfUMB8GA1UdIwQYMBaAFJ6VLlNm0WVGHVj9
# l9KLVBjNmWoeMIHCBgNVHR8EgbowgbcwgbSggbGgga6GgatsZGFwOi8vL0NOPU9U
# Q0ZTQS1DQSxDTj1XTENLMDUsQ049Q0RQLENOPVB1YmxpYyUyMEtleSUyMFNlcnZp
# Y2VzLENOPVNlcnZpY2VzLENOPUNvbmZpZ3VyYXRpb24sREM9b3RjZixEQz1wbD9j
# ZXJ0aWZpY2F0ZVJldm9jYXRpb25MaXN0P2Jhc2U/b2JqZWN0Q2xhc3M9Y1JMRGlz
# dHJpYnV0aW9uUG9pbnQwgbcGCCsGAQUFBwEBBIGqMIGnMIGkBggrBgEFBQcwAoaB
# l2xkYXA6Ly8vQ049T1RDRlNBLUNBLENOPUFJQSxDTj1QdWJsaWMlMjBLZXklMjBT
# ZXJ2aWNlcyxDTj1TZXJ2aWNlcyxDTj1Db25maWd1cmF0aW9uLERDPW90Y2YsREM9
# cGw/Y0FDZXJ0aWZpY2F0ZT9iYXNlP29iamVjdENsYXNzPWNlcnRpZmljYXRpb25B
# dXRob3JpdHkwLAYDVR0RBCUwI6AhBgorBgEEAYI3FAIDoBMMEXBpb2ttaWFkbUBv
# dGNmLnBsMA0GCSqGSIb3DQEBCwUAA4IBAQBHgFkPEIh/P8coDdg02kio/uDPfhTS
# HUsVOccNyHXb7JWgBNZfT1YL/pg4ess12zUYl4MZ/loUugwreEnQgdm0QyVip3Ki
# +i0OzehzC3jSFRIMrTinScLWuZFmMpyb91VQX0iWNdCkbADNjawUYL1VymEKKQZl
# D0d+lhquaNvo979wpHmjS1DRcjeOKpnQpTfbetwtFtLKRBsHaKnbSFCd9ZV7g3hJ
# qbMeLCSAXzSKKEO6XmMruE6wRJNSCS0lXr13BDJQRhzeh7CBKZ6p5fATbVCxGzfj
# RPTaJq9gYm2bb0Jgc+Sfqmp5Lnx/XHFgB+1p8KqAcRfCB0eJnnDAmDw0MYIB9jCC
# AfICAQEwVTA+MRIwEAYKCZImiZPyLGQBGRYCcGwxFDASBgoJkiaJk/IsZAEZFgRv
# dGNmMRIwEAYDVQQDEwlPVENGU0EtQ0ECE3MAAAPpayrIKlGbX8MAAAAAA+kwCQYF
# Kw4DAhoFAKB4MBgGCisGAQQBgjcCAQwxCjAIoAKAAKECgAAwGQYJKoZIhvcNAQkD
# MQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEOMAwGCisGAQQBgjcCARUwIwYJ
# KoZIhvcNAQkEMRYEFJD3eFTQytsOFpvcKY36583ssmnuMA0GCSqGSIb3DQEBAQUA
# BIIBAE591vV6bXE2N5uZLhCt4Bx11aHxfa6CqbBjdb0HaYzg1dyuBam+jxYfDU6W
# vBabR79DaUry2ZvzfltCr3uDofs6SGAHUXpTSf2Ivy57YIC4jkNq+3n3/yQEjBdt
# 9o+VA5bsd0SPfdfSnzatyzp0ICm+IXtFmVkoXckt57kAhca9B3VaYxpprc2MDLIo
# 0qujzADD9guxR1jbEkWWg+r2VtKnBExejTLgmagEiCLTcKM4A7dvVC3PGOmRIjXm
# MyDGNyJu/T75WAmga74WnWxVgjq8X7A0IIuB8k24SRgsceRuT0f4Hbqg10oCPFV2
# XqQ2KQ5MSmX0TRYLR+UjC1pXAIA=
# SIG # End signature block
