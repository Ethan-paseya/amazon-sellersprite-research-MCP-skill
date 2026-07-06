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
    ".claude\skills\amazon-analyse\references\runtime-credential-preflight.md",
    ".claude\skills\amazon-analyse\references\sellersprite-mcp-api.md",
    ".claude\skills\category-selection\SKILL.md",
    ".claude\skills\category-selection\references\runtime-credential-preflight.md",
    ".claude\skills\category-selection\references\sellersprite-mcp-api.md",
    ".claude\skills\keyword-research\SKILL.md",
    ".claude\skills\keyword-research\references\runtime-credential-preflight.md",
    ".claude\skills\keyword-research\references\sellersprite-mcp-api.md",
    ".claude\skills\review-analysis\SKILL.md",
    ".claude\skills\review-analysis\references\runtime-credential-preflight.md",
    ".claude\skills\review-analysis\references\sellersprite-mcp-api.md",
    ".claude\skills\product-research\SKILL.md",
    ".claude\skills\product-research\references\runtime-credential-preflight.md",
    ".claude\skills\product-research\references\sellersprite-mcp-api.md",
    ".claude\skills\product-planning\SKILL.md",
    ".claude\skills\product-planning\references\product-planning-mcp-flow.zh.md",
    ".claude\skills\product-planning\references\runtime-credential-preflight.md",
    ".claude\skills\product-planning\references\sellersprite-mcp-api.md",
    ".claude\skills\product-planning\references\planning-workflow.md",
    "skills\amazon-analyse\SKILL.md",
    "skills\amazon-analyse\references\runtime-credential-preflight.md",
    "skills\amazon-analyse\references\sellersprite-mcp-api.md",
    "skills\category-selection\SKILL.md",
    "skills\category-selection\references\runtime-credential-preflight.md",
    "skills\category-selection\references\sellersprite-mcp-api.md",
    "skills\keyword-research\SKILL.md",
    "skills\keyword-research\references\runtime-credential-preflight.md",
    "skills\keyword-research\references\sellersprite-mcp-api.md",
    "skills\review-analysis\SKILL.md",
    "skills\review-analysis\references\runtime-credential-preflight.md",
    "skills\review-analysis\references\sellersprite-mcp-api.md",
    "skills\product-research\SKILL.md",
    "skills\product-research\references\runtime-credential-preflight.md",
    "skills\product-research\references\sellersprite-mcp-api.md",
    "skills\product-planning\SKILL.md",
    "skills\product-planning\references\product-planning-mcp-flow.zh.md",
    "skills\product-planning\references\runtime-credential-preflight.md",
    "skills\product-planning\references\sellersprite-mcp-api.md",
    "skills\product-planning\references\planning-workflow.md",
    "docs\sellersprite-mcp-usage.zh.md",
    "docs\python-tools.md",
    "references\product-planning-mcp-flow.zh.md",
    "references\runtime-credential-preflight.md",
    "references\sellersprite-mcp-api.md",
    "scripts\python\sellersprite_skill_tools.py",
    "scripts\python\scan_sensitive.py",
    "scripts\python\check_runtime_config.py",
    "scripts\python\check_package.py",
    "scripts\python\test_open_source_skills.py",
    "scripts\python\install_skill.py",
    "scripts\python\publish_github_api.py",
    "scripts\python\create_placeholder_template.py",
    "templates\amazon-single-product-report.zh.md",
    "templates\product-planning-report.zh.md",
    "templates\product-planning-meeting-workbook-layout.zh.md",
    "templates\product-planning-workbook-layout.md",
    "templates\amazon_single_product_meeting_template.xlsx",
    "templates\product_planning_standard_template_V1.xlsx",
    "templates\product_planning_standard_template_V1_manifest.json",
    "reports\README.md",
    "category-reports\README.md",
    "keyword-reports\README.md",
    "review-analysis-reports\README.md",
    "product-research-reports\README.md",
    "product-planning-reports\README.md"
)

foreach ($item in $required) {
    $full = Join-Path $Path $item
    if (!(Test-Path $full)) {
        throw "Missing required file: $item"
    }
}

Write-Host "Checking Excel template packages..."
Add-Type -AssemblyName System.IO.Compression.FileSystem
$xlsxFiles = @(
    "templates\amazon_single_product_meeting_template.xlsx",
    "templates\product_planning_standard_template_V1.xlsx"
)

foreach ($xlsxFile in $xlsxFiles) {
    $xlsx = Join-Path $Path $xlsxFile
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
}

Write-Host "Package check passed."
