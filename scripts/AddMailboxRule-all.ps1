# All Users
$Users = @("akim", "jreyes", "mpatel", "rchen", "talvarez")

# Loop through all users and add mailbox rule
foreach ($User in $Users) {
    .\AddMailboxRule.ps1 $User
}
