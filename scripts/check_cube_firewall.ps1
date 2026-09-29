$ErrorActionPreference = 'Stop'

try {
    $profiles = @(Get-NetFirewallProfile -PolicyStore ActiveStore)
} catch {
    Write-Error "Unable to read active Windows Firewall profiles: $($_.Exception.Message)"
    exit 1
}

$unsafeProfiles = @($profiles | Where-Object {
    -not $_.Enabled -or $_.DefaultInboundAction -ne 'Block'
})
if ($profiles.Count -lt 3 -or $unsafeProfiles.Count -gt 0) {
    Write-Error 'Safety check failed: Domain, Private, and Public profiles must all be enabled with inbound default Block. Do not start Cube; contact workstation IT if policy needs review.'
    $profiles | Select-Object Name, Enabled, DefaultInboundAction | Format-Table -AutoSize
    exit 1
}

try {
    $allowRules = @(Get-NetFirewallRule -PolicyStore ActiveStore -Enabled True -Direction Inbound -Action Allow)
    $nodeCubeRules = foreach ($rule in $allowRules) {
        $application = Get-NetFirewallApplicationFilter -AssociatedNetFirewallRule $rule -ErrorAction SilentlyContinue
        $program = [string]$application.Program
        if ($rule.DisplayName -match '(?i)node|cube' -or
            $rule.Name -match '(?i)node|cube' -or
            $program -match '(?i)(^|[\\/])node(?:\.exe)?$|cube') {
            [pscustomobject]@{
                Name = $rule.Name
                DisplayName = $rule.DisplayName
                Program = $program
                Profile = $rule.Profile
            }
        }
    }
} catch {
    Write-Error "Unable to verify active inbound allow rules: $($_.Exception.Message)"
    exit 1
}

if (@($nodeCubeRules).Count -gt 0) {
    Write-Error 'Safety check failed: an enabled inbound allow rule matching Node/Cube exists. Do not start Cube; contact workstation IT.'
    $nodeCubeRules | Format-List
    exit 1
}

$profiles | Select-Object Name, Enabled, DefaultInboundAction | Format-Table -AutoSize
Write-Output 'PASS: all firewall profiles are enabled and inbound-blocking; no enabled Node/Cube inbound allow rule was found.'
Write-Output 'This check is read-only. It does not change firewall policy.'
