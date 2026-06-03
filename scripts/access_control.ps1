# Access Control Enforcement Script
# Verifies only authorized users can trigger deployments

param(
    [string]$GitHubActor,
    [string]$AuthorizedUsersFile = "config/authorized_users.txt"
)

# Read authorized users list
$authorizedUsers = Get-Content $AuthorizedUsersFile

# Check if the deploying user is authorized
if ($authorizedUsers -contains $GitHubActor) {
    Write-Host " Access granted: $GitHubActor is authorized to deploy"
    exit 0
} else {
    Write-Host " Access denied: $GitHubActor is not authorized to deploy"
    exit 1
}
