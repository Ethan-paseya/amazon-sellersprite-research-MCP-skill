param(
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path $Path
$skills = @("amazon-analyse", "category-selection", "keyword-research", "review-analysis", "product-research", "product-planning")

Write-Host "Testing open-source skill business logic..."

$requiredRootFiles = @(
    "references\runtime-credential-preflight.md",
    "references\sellersprite-mcp-api.md",
    ".env.example",
    ".mcp.json.example"
)

foreach ($item in $requiredRootFiles) {
    $full = Join-Path $root $item
    if (!(Test-Path -LiteralPath $full)) {
        throw "Missing required open-source support file: $item"
    }
}

$forbiddenRuntimeFiles = @(".env", ".mcp.json")
foreach ($item in $forbiddenRuntimeFiles) {
    $full = Join-Path $root $item
    if (Test-Path -LiteralPath $full) {
        throw "Runtime secret-bearing file must not exist in open-source package: $item"
    }
}

foreach ($skill in $skills) {
    foreach ($family in @("skills", ".claude\skills")) {
        $skillDir = Join-Path $root "$family\$skill"
        $skillMd = Join-Path $skillDir "SKILL.md"
        if (!(Test-Path -LiteralPath $skillMd)) {
            throw "Missing SKILL.md: $family\$skill"
        }

        $text = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillMd
        if ($text -notmatch "Credential Preflight") {
            throw "Missing Credential Preflight section: $family\$skill"
        }
        if ($text -notmatch "runtime-credential-preflight\.md") {
            throw "Skill does not reference runtime credential preflight: $family\$skill"
        }
        if ($text -notmatch "SellerSprite MCP API key") {
            throw "Skill does not explicitly request SellerSprite key when missing: $family\$skill"
        }
        if ($text -notmatch "Gemini/GLM|Gemini or GLM") {
            throw "Skill does not explicitly handle Gemini/GLM validation keys: $family\$skill"
        }

        $runtimeRef = Join-Path $skillDir "references\runtime-credential-preflight.md"
        $mcpRef = Join-Path $skillDir "references\sellersprite-mcp-api.md"
        if (!(Test-Path -LiteralPath $runtimeRef)) {
            throw "Missing bundled runtime credential reference: $family\$skill"
        }
        if (!(Test-Path -LiteralPath $mcpRef)) {
            throw "Missing bundled SellerSprite MCP reference: $family\$skill"
        }
    }
}

Write-Host "Running sensitive-content scan..."
powershell -ExecutionPolicy Bypass -File (Join-Path $root "scripts\scan-sensitive.ps1") -Path $root

Write-Host "Open-source skill logic test passed."
