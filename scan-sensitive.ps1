param(
    [string]$Path = "."
)

$ErrorActionPreference = "Stop"

$patterns = @(
    @{ Label = "Google/Gemini API key"; Regex = "AIza[0-9A-Za-z_\-]{20,}" },
    @{ Label = "GitHub token"; Regex = "(github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[0-9A-Za-z_]{20,}" },
    @{ Label = "GLM/BigModel API key"; Regex = "[0-9a-fA-F]{32}\.[0-9A-Za-z_\-]{8,}" },
    @{ Label = "Gemini env value"; Regex = "GEMINI_API_KEY\s*=\s*(?!YOUR|YOUR_GEMINI_API_KEY|`$\{GEMINI_API_KEY\}|$)[^\s]+" },
    @{ Label = "GLM env value"; Regex = "GLM_API_KEY\s*=\s*(?!YOUR|YOUR_GLM_API_KEY|`$\{GLM_API_KEY\}|$)[^\s]+" },
    @{ Label = "SellerSprite env value"; Regex = 'SELLERSPRITE_API_KEY\s*=\s*(?!YOUR|YOUR_SELLERSPRITE_API_KEY|\$\{SELLERSPRITE_API_KEY\}|$)[^\s]+' },
    @{ Label = "SellerSprite URL secret"; Regex = "https://mcp\.sellersprite\.com/mcp\?secret-key=(?!YOUR|YOUR_SELLERSPRITE_API_KEY)[0-9A-Za-z._\-]+" },
    @{ Label = "SellerSprite header secret"; Regex = '"secret-key"\s*:\s*"(?!YOUR|\$\{SELLERSPRITE_API_KEY\})[0-9A-Za-z._\-]+"' },
    @{ Label = "Local Windows user path"; Regex = "C:[\\/]+Users[\\/]+ETHAN" },
    @{ Label = "Real-looking ASIN"; Regex = "\bB0[A-Z0-9]{8}\b" }
)

$excludeDirs = @(".git", "node_modules", "__pycache__")
$files = Get-ChildItem -Path $Path -Recurse -File | Where-Object {
    $full = $_.FullName
    -not ($excludeDirs | Where-Object { $full -like "*\$_\*" })
}

$findings = New-Object System.Collections.Generic.List[string]

function Test-TextForSensitiveContent {
    param(
        [string]$Text,
        [string]$Source
    )

    foreach ($pattern in $patterns) {
        if ($Text -match $pattern.Regex) {
            $findings.Add("$Source :: $($pattern.Label)")
        }
    }
}

function Test-ZipPackageForSensitiveContent {
    param([System.IO.FileInfo]$File)

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [System.IO.Compression.ZipFile]::OpenRead($File.FullName)
    try {
        foreach ($entry in $zip.Entries) {
            $entryName = $entry.FullName
            $entryExt = [System.IO.Path]::GetExtension($entryName).ToLowerInvariant()
            if ($entryExt -notin @(".xml", ".rels", ".txt", ".json", ".csv")) {
                continue
            }

            $reader = New-Object IO.StreamReader($entry.Open())
            try {
                $text = $reader.ReadToEnd()
                Test-TextForSensitiveContent -Text $text -Source "$($File.FullName)!$entryName"
            }
            finally {
                $reader.Close()
            }
        }
    }
    finally {
        $zip.Dispose()
    }
}

foreach ($file in $files) {
    $ext = [System.IO.Path]::GetExtension($file.Name).ToLowerInvariant()
    if ($ext -in @(".xlsx", ".docx", ".pptx")) {
        Test-ZipPackageForSensitiveContent -File $file
        continue
    }

    if ($ext -in @(".png", ".jpg", ".jpeg", ".gif", ".bin", ".ico", ".pdf")) {
        continue
    }

    $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
    Test-TextForSensitiveContent -Text $text -Source $file.FullName
}

if ($findings.Count -eq 0) {
    Write-Host "No obvious sensitive patterns found."
    exit 0
}

Write-Host "Potential sensitive content found:"
$findings | ForEach-Object { Write-Host $_ }
exit 1
