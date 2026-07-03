param(
    [ValidateSet("claude", "codex")]
    [string]$Target = "codex",

    [ValidateSet("all", "amazon-analyse", "category-selection", "keyword-research", "review-analysis", "product-research")]
    [string]$Skill = "all"
)

$ErrorActionPreference = "Stop"

$repo = Resolve-Path (Join-Path $PSScriptRoot "..")
$skillNames = @("amazon-analyse", "category-selection", "keyword-research", "review-analysis", "product-research")
if ($Skill -ne "all") {
    $skillNames = @($Skill)
}

if ($Target -eq "claude") {
    $destRoot = Join-Path $env:USERPROFILE ".claude\skills"
    $srcRoot = Join-Path $repo ".claude\skills"
} else {
    $destRoot = Join-Path $env:USERPROFILE ".codex\skills"
    $srcRoot = Join-Path $repo "skills"
}

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

foreach ($name in $skillNames) {
    $src = Join-Path $srcRoot $name
    if (!(Test-Path $src)) {
        throw "Missing skill source: $src"
    }
    Copy-Item -Recurse -Force -LiteralPath $src -Destination $destRoot
    Write-Host "Installed $name to $destRoot"
}
