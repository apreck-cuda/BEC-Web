param (
    [string]$Username = "jreyes",
    [string]$RuleName = "Rule"
)

# Define allowed Usernames
$ValidUsernames = @("akim", "jreyes", "mpatel", "rchen", "talvarez")

# Validate Username
if ($ValidUsernames -contains $Username) {
    $Mailbox = "$Username@barracudademo.com"
    Write-Host "Using Mailbox: $Mailbox"
} else {
    Write-Host "Invalid Username. Allowed values are: $($ValidUsernames -join ', ')"
    exit
}

# Generate a random 5-character string
$RandomSuffix = -join ((65..90) + (97..122) | Get-Random -Count 5 | ForEach-Object {[char]$_})

# Append the random string to the RuleName
$RuleName += "_$RandomSuffix"

# Output the updated RuleName
Write-Output "Updated RuleName: $RuleName"

# Ensure TLS 1.2 is configured for PowerShell session
[Net.ServicePointManager]::SecurityProtocol =
    [Net.ServicePointManager]::SecurityProtocol -bor
    [Net.SecurityProtocolType]::Tls12

# Connect to Exchange Online
#Connect-ExchangeOnline -UserPrincipalName awelch@barracudademo.com `
#                       -ShowBanner:$false

# Connect to Exchange Online using Managed Identity
Connect-ExchangeOnline -ManagedIdentity -ManagedIdentityAccountId  69d8d06c-c2d8-4499-95bf-d30c39ed43b7 -Organization barracudademotenant.onmicrosoft.com  -ShowBanner:$false

#Get all inbox rules
$rules = Get-InboxRule -Mailbox $Mailbox

# Loop through and delete each rule
foreach ($rule in $rules) {
    Write-Host "Deleting rule: $($rule.Name)"
    Remove-InboxRule -Identity $rule.Identity -Confirm:$false
}

#Create the rule
New-InboxRule -Mailbox $Mailbox `
              -Name $RuleName `
              -SubjectContainsWords "Mailer-Daemon", "Failure Notice" `
              -BodyContainsWords "Mailer-Daemon", "Failure Notice" `
              -DeleteMessage $true `
              -StopProcessingRules $true

# Disconnect session
Disconnect-ExchangeOnline -Confirm:$false