param(
    [string]$Path = ".",
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path $Path
$envPath = Join-Path $root ".env"
$mcpPath = Join-Path $root ".mcp.json"

function Read-DotEnv {
    param([string]$FilePath)

    $values = @{}
    if (!(Test-Path -LiteralPath $FilePath)) {
        return $values
    }

    foreach ($line in Get-Content -LiteralPath $FilePath) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith("#")) {
            continue
        }
        $idx = $trimmed.IndexOf("=")
        if ($idx -le 0) {
            continue
        }
        $name = $trimmed.Substring(0, $idx).Trim()
        $value = $trimmed.Substring($idx + 1).Trim()
        $values[$name] = $value
    }

    return $values
}

function Test-RealValue {
    param(
        [string]$Value,
        [string[]]$Placeholders
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return $false
    }
    if ($Value.StartsWith("YOUR_")) {
        return $false
    }
    if ($Value.StartsWith('${') -and $Value.EndsWith('}')) {
        return $false
    }
    return -not ($Placeholders -contains $Value)
}

$dotenv = Read-DotEnv -FilePath $envPath
$checks = @(
    @{ Name = "SELLERSPRITE_API_KEY"; Purpose = "SellerSprite MCP data"; Placeholder = @("YOUR_SELLERSPRITE_API_KEY", "YOUR_KEY"); Default = $null },
    @{ Name = "GEMINI_API_KEY"; Purpose = "Gemini validation"; Placeholder = @("YOUR_GEMINI_API_KEY"); Default = $null },
    @{ Name = "GLM_API_KEY"; Purpose = "GLM validation"; Placeholder = @("YOUR_GLM_API_KEY"); Default = $null },
    @{ Name = "GLM_BASE_URL"; Purpose = "GLM endpoint"; Placeholder = @("YOUR_GLM_BASE_URL"); Default = "https://open.bigmodel.cn/api/paas/v4" }
)

$rows = New-Object System.Collections.Generic.List[object]
foreach ($check in $checks) {
    $value = $null
    if ($dotenv.ContainsKey($check.Name)) {
        $value = $dotenv[$check.Name]
    }
    elseif ([Environment]::GetEnvironmentVariable($check.Name)) {
        $value = [Environment]::GetEnvironmentVariable($check.Name)
    }

    $source = "missing"
    if ($dotenv.ContainsKey($check.Name)) {
        $source = ".env"
    }
    elseif ([Environment]::GetEnvironmentVariable($check.Name)) {
        $source = "environment"
    }
    elseif ($check.Default) {
        $value = $check.Default
        $source = "default"
    }

    $configured = Test-RealValue -Value $value -Placeholders $check.Placeholder
    $rows.Add([pscustomobject]@{
        Name = $check.Name
        Purpose = $check.Purpose
        Configured = $configured
        Source = $source
    })
}

$mcpConfigured = $false
if (Test-Path -LiteralPath $mcpPath) {
    $mcpText = Get-Content -Raw -LiteralPath $mcpPath
    $mcpConfigured = ($mcpText -match '"url"\s*:\s*"https://mcp\.sellersprite\.com/mcp"') -and ($mcpText -match '"secret-key"\s*:')
}

$rows.Add([pscustomobject]@{
    Name = ".mcp.json sellersprite"
    Purpose = "MCP server registration"
    Configured = $mcpConfigured
    Source = $(if (Test-Path -LiteralPath $mcpPath) { ".mcp.json" } else { "missing" })
})

$rows | Format-Table -AutoSize

$missing = @($rows | Where-Object { -not $_.Configured })
if ($missing.Count -gt 0) {
    Write-Host "Missing or placeholder-only runtime configuration:"
    $missing | ForEach-Object { Write-Host "- $($_.Name): $($_.Purpose)" }
    Write-Host "Provide the missing keys at runtime, or configure local ignored .env/.mcp.json files."
    if ($Strict) {
        exit 1
    }
}
else {
    Write-Host "Runtime configuration looks complete. Values were not printed."
}
