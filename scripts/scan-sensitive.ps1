param(
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

$patterns = @(
    "AIza[0-9A-Za-z_\-]{20,}",
    "secret-key=[0-9a-fA-F]{16,}",
    "bf[0-9a-fA-F]{20,}",
    "GEMINI_API_KEY\s*=\s*[^Y\s].+",
    "GLM_API_KEY\s*=\s*[^Y\s].+",
    "SELLERSPRITE_MCP_URL\s*=\s*https://mcp\.sellersprite\.com/mcp\?secret-key=(?!YOUR)",
    "B0[A-Z0-9]{8}"
)

$excludeDirs = @(".git", "node_modules")
$files = Get-ChildItem -Path $Path -Recurse -File | Where-Object {
    $full = $_.FullName
    -not ($excludeDirs | Where-Object { $full -like "*\$_\*" })
}

$findings = New-Object System.Collections.Generic.List[string]
foreach ($file in $files) {
    $ext = [System.IO.Path]::GetExtension($file.Name).ToLowerInvariant()
    if ($ext -in @(".xlsx", ".png", ".jpg", ".jpeg", ".gif", ".bin")) {
        continue
    }
    $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    foreach ($pattern in $patterns) {
        if ($text -match $pattern) {
            $findings.Add("$($file.FullName) :: $pattern")
        }
    }
}

if ($findings.Count -eq 0) {
    Write-Host "No obvious sensitive patterns found."
    exit 0
}

Write-Host "Potential sensitive content found:"
$findings | ForEach-Object { Write-Host $_ }
exit 1
