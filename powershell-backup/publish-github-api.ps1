param(
    [string]$RepoName = "amazon-sellersprite-research-MCP-skill",
    [string]$Description = "SellerSprite MCP based Amazon research skills for listing, category, keyword, review, and product opportunity analysis.",
    [string]$Branch = "main",
    [switch]$Private
)

$ErrorActionPreference = "Stop"

$token = [Environment]::GetEnvironmentVariable("GITHUB_TOKEN")
if ([string]::IsNullOrWhiteSpace($token)) {
    throw "Missing GITHUB_TOKEN. Set it only for the current shell, then rerun: `$env:GITHUB_TOKEN='YOUR_TOKEN'"
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

function Invoke-GitHubJson {
    param(
        [string]$Method,
        [string]$Uri,
        [object]$Body = $null,
        [switch]$Allow404
    )

    try {
        if ($null -eq $Body) {
            return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $headers
        }
        $json = $Body | ConvertTo-Json -Depth 10
        return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $headers -Body $json -ContentType "application/json"
    }
    catch {
        $response = $_.Exception.Response
        if ($Allow404 -and $null -ne $response -and [int]$response.StatusCode -eq 404) {
            return $null
        }
        throw
    }
}

$me = Invoke-GitHubJson -Method GET -Uri "https://api.github.com/user"
$owner = $me.login

$repo = Invoke-GitHubJson -Method GET -Uri "https://api.github.com/repos/$owner/$RepoName" -Allow404
if ($null -eq $repo) {
    Write-Host "Creating repository $owner/$RepoName..."
    $repo = Invoke-GitHubJson -Method POST -Uri "https://api.github.com/user/repos" -Body @{
        name = $RepoName
        description = $Description
        private = [bool]$Private
        auto_init = $false
    }
}
else {
    Write-Host "Repository already exists: $owner/$RepoName"
}

$excludeDirs = @("\.git\", "\reports\", "\category-reports\", "\keyword-reports\", "\review-analysis-reports\", "\product-research-reports\", "\product-planning-reports\")
$files = Get-ChildItem -Path $root -Recurse -File | Where-Object {
    $full = $_.FullName
    $relative = $full.Substring($root.Path.Length + 1)
    if ($relative -in @(".env", ".mcp.json")) { return $false }
    foreach ($dir in $excludeDirs) {
        if ($full.Contains($dir)) {
            if ($_.Name -in @("README.md", ".gitkeep")) { return $true }
            return $false
        }
    }
    return $true
}

foreach ($file in $files) {
    $relative = $file.FullName.Substring($root.Path.Length + 1).Replace("\", "/")
    $encodedPath = [System.Uri]::EscapeDataString($relative).Replace("%2F", "/")
    $uri = "https://api.github.com/repos/$owner/$RepoName/contents/$encodedPath"
    $existing = Invoke-GitHubJson -Method GET -Uri $uri -Allow404
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    $content = [Convert]::ToBase64String($bytes)

    $body = @{
        message = "Add $relative"
        content = $content
        branch = $Branch
    }
    if ($null -ne $existing -and $existing.sha) {
        $body.sha = $existing.sha
        $body.message = "Update $relative"
    }

    Write-Host "Uploading $relative"
    Invoke-GitHubJson -Method PUT -Uri $uri -Body $body | Out-Null
}

Write-Host "Done: https://github.com/$owner/$RepoName"
