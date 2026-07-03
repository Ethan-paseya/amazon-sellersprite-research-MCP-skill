param(
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

Write-Host "Running sensitive-content scan..."
powershell -ExecutionPolicy Bypass -File (Join-Path $Path "scripts\scan-sensitive.ps1") -Path $Path

Write-Host "Checking required files..."
$required = @(
    "README.md",
    ".env.example",
    ".mcp.json.example",
    "CLAUDE.md",
    "SECURITY.md",
    ".claude\skills\amazon-analyse\SKILL.md",
    ".claude\skills\category-selection\SKILL.md",
    ".claude\skills\keyword-research\SKILL.md",
    ".claude\skills\review-analysis\SKILL.md",
    ".claude\skills\product-research\SKILL.md",
    "skills\amazon-analyse\SKILL.md",
    "skills\category-selection\SKILL.md",
    "skills\keyword-research\SKILL.md",
    "skills\review-analysis\SKILL.md",
    "skills\product-research\SKILL.md",
    "references\sellersprite-mcp-api.md",
    "templates\amazon-single-product-report.zh.md",
    "templates\amazon_single_product_meeting_template.xlsx",
    "reports\README.md",
    "category-reports\README.md",
    "keyword-reports\README.md",
    "review-analysis-reports\README.md",
    "product-research-reports\README.md"
)

foreach ($item in $required) {
    $full = Join-Path $Path $item
    if (!(Test-Path $full)) {
        throw "Missing required file: $item"
    }
}

Write-Host "Checking Excel template package..."
Add-Type -AssemblyName System.IO.Compression.FileSystem
$xlsx = Join-Path $Path "templates\amazon_single_product_meeting_template.xlsx"
$zip = [System.IO.Compression.ZipFile]::OpenRead((Resolve-Path $xlsx))
try {
    foreach ($entry in $zip.Entries | Where-Object { $_.FullName.EndsWith(".xml") }) {
        $reader = New-Object IO.StreamReader($entry.Open())
        $xml = $reader.ReadToEnd()
        $reader.Close()
        [xml]$null = $xml
    }
}
finally {
    $zip.Dispose()
}

Write-Host "Package check passed."
