param(
    [string]$OutputPath = "templates\amazon_single_product_meeting_template.xlsx"
)

$ErrorActionPreference = "Stop"

function X([object]$Value) {
    if ($null -eq $Value) { return "" }
    return [System.Security.SecurityElement]::Escape([string]$Value)
}

function ColName([int]$Index) {
    $name = ""
    while ($Index -gt 0) {
        $mod = ($Index - 1) % 26
        $name = [char](65 + $mod) + $name
        $Index = [math]::Floor(($Index - $mod) / 26)
    }
    return $name
}

function CellXml([int]$Col, [int]$Row, [object]$Value, [int]$Style = 0) {
    $ref = "$(ColName $Col)$Row"
    $styleAttr = if ($Style -gt 0) { " s=`"$Style`"" } else { "" }
    if ($null -eq $Value -or $Value -eq "") { return "<c r=`"$ref`"$styleAttr/>" }
    return "<c r=`"$ref`" t=`"inlineStr`"$styleAttr><is><t>$(X $Value)</t></is></c>"
}

function RowXml([int]$Row, [object[]]$Values, [int[]]$Styles = @()) {
    $cells = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $Values.Count; $i++) {
        $style = if ($i -lt $Styles.Count) { $Styles[$i] } else { 0 }
        $cells.Add((CellXml ($i + 1) $Row $Values[$i] $style))
    }
    return "<row r=`"$Row`">$($cells -join '')</row>"
}

function SheetXml([array]$Rows, [array]$Widths, [int]$FreezeRow = 1, [string]$AutoFilter = "", [string]$MergeCells = "") {
    $body = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $Rows.Count; $i++) {
        $values = [object[]]$Rows[$i].Values
        $styles = if ($Rows[$i].Styles) { [int[]]$Rows[$i].Styles } else { @() }
        $body.Add((RowXml ($i + 1) $values $styles))
    }
    $lastCol = 1
    foreach ($r in $Rows) { if ($r.Values.Count -gt $lastCol) { $lastCol = $r.Values.Count } }
    $lastRow = $Rows.Count
    $cols = for ($i = 0; $i -lt $Widths.Count; $i++) {
        $idx = $i + 1
        "<col min=`"$idx`" max=`"$idx`" width=`"$($Widths[$i])`" customWidth=`"1`"/>"
    }
    $pane = if ($FreezeRow -gt 0) { "<pane ySplit=`"$FreezeRow`" topLeftCell=`"A$($FreezeRow + 1)`" activePane=`"bottomLeft`" state=`"frozen`"/><selection pane=`"bottomLeft`" activeCell=`"A$($FreezeRow + 1)`" sqref=`"A$($FreezeRow + 1)`"/>" } else { "<selection activeCell=`"A1`" sqref=`"A1`"/>" }
    $filter = if ($AutoFilter) { "<autoFilter ref=`"$AutoFilter`"/>" } else { "" }
    $merges = if ($MergeCells) { "<mergeCells count=`"1`"><mergeCell ref=`"$MergeCells`"/></mergeCells>" } else { "" }
    return @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="A1:$(ColName $lastCol)$lastRow"/>
  <sheetViews><sheetView showGridLines="0" workbookViewId="0">$pane</sheetView></sheetViews>
  <sheetFormatPr defaultRowHeight="18"/>
  <cols>$($cols -join '')</cols>
  <sheetData>$($body -join '')</sheetData>
  $filter
  $merges
</worksheet>
"@
}

function SaveText([string]$Path, [string]$Text) {
    $dir = Split-Path $Path -Parent
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    [System.IO.File]::WriteAllText($Path, $Text, [System.Text.UTF8Encoding]::new($false))
}

$sheets = @(
    @{
        Name = "会议摘要"
        Widths = @(20, 52, 18, 18, 18, 18)
        Merge = "A1:F1"
        Filter = ""
        Rows = @(
            @{ Values = @("{{PRODUCT_TITLE}} 产品经理会议版", "", "", "", "", ""); Styles = @(1,1,1,1,1,1) },
            @{ Values = @("会议目标", "{{MEETING_GOAL}}", "", "", "", ""); Styles = @(2,0,0,0,0,0) },
            @{ Values = @("ASIN", "{{ASIN}}", "品牌", "{{BRAND}}", "站点", "{{SITE}}"); Styles = @(2,0,2,0,2,0) },
            @{ Values = @("价格", "{{PRICE}}", "评分", "{{RATING}}", "评论数", "{{RATINGS_COUNT}}"); Styles = @(2,0,2,0,2,0) },
            @{ Values = @("PM结论", "{{PM_CONCLUSION}}", "", "", "", ""); Styles = @(2,0,0,0,0,0) }
        )
    },
    @{
        Name = "产品基础信息"
        Widths = @(18, 46, 34, 34)
        Merge = ""
        Filter = "A1:D6"
        Rows = @(
            @{ Values = @("字段", "内容", "PM解读", "会议关注点"); Styles = @(2,2,2,2) },
            @{ Values = @("标题", "{{PRODUCT_TITLE}}", "{{TITLE_INSIGHT}}", "{{TITLE_DISCUSSION}}") },
            @{ Values = @("类目", "{{CATEGORY}}", "{{CATEGORY_INSIGHT}}", "{{CATEGORY_DISCUSSION}}") },
            @{ Values = @("价格", "{{PRICE}}", "{{PRICE_INSIGHT}}", "{{PRICE_DISCUSSION}}") },
            @{ Values = @("评分", "{{RATING}}", "{{RATING_INSIGHT}}", "{{RATING_DISCUSSION}}") },
            @{ Values = @("核心卖点", "{{FEATURES}}", "{{FEATURE_INSIGHT}}", "{{FEATURE_DISCUSSION}}") }
        )
    },
    @{
        Name = "销售趋势"
        Widths = @(14, 14, 14, 28, 16, 28)
        Merge = ""
        Filter = "A1:F8"
        Rows = @(
            @{ Values = @("月份", "价格", "销量", "销量条", "销售额", "销售额条"); Styles = @(2,2,2,2,2,2) },
            @{ Values = @("{{MONTH_1}}", "{{PRICE_1}}", "{{UNITS_1}}", "{{UNITS_BAR_1}}", "{{REVENUE_1}}", "{{REVENUE_BAR_1}}") },
            @{ Values = @("{{MONTH_2}}", "{{PRICE_2}}", "{{UNITS_2}}", "{{UNITS_BAR_2}}", "{{REVENUE_2}}", "{{REVENUE_BAR_2}}") }
        )
    },
    @{
        Name = "关键词布局"
        Widths = @(28, 14, 14, 12, 12, 12, 28, 44)
        Merge = ""
        Filter = "A1:H8"
        Rows = @(
            @{ Values = @("关键词", "搜索量", "购买量", "购买率", "CPC", "流量占比", "占比条", "PM解读"); Styles = @(2,2,2,2,2,2,2,2) },
            @{ Values = @("{{KEYWORD_1}}", "{{SEARCHES_1}}", "{{PURCHASES_1}}", "{{PURCHASE_RATE_1}}", "{{CPC_1}}", "{{TRAFFIC_SHARE_1}}", "{{TRAFFIC_BAR_1}}", "{{KEYWORD_NOTE_1}}") },
            @{ Values = @("{{KEYWORD_2}}", "{{SEARCHES_2}}", "{{PURCHASES_2}}", "{{PURCHASE_RATE_2}}", "{{CPC_2}}", "{{TRAFFIC_SHARE_2}}", "{{TRAFFIC_BAR_2}}", "{{KEYWORD_NOTE_2}}") }
        )
    },
    @{
        Name = "评论VOC"
        Widths = @(24, 12, 12, 50, 54)
        Merge = ""
        Filter = "A1:E8"
        Rows = @(
            @{ Values = @("问题/优势类型", "样本数", "严重度", "证据摘要", "产品动作"); Styles = @(2,2,2,2,2) },
            @{ Values = @("{{VOC_TYPE_1}}", "{{VOC_COUNT_1}}", "{{VOC_SEVERITY_1}}", "{{VOC_EVIDENCE_1}}", "{{VOC_ACTION_1}}") },
            @{ Values = @("{{VOC_TYPE_2}}", "{{VOC_COUNT_2}}", "{{VOC_SEVERITY_2}}", "{{VOC_EVIDENCE_2}}", "{{VOC_ACTION_2}}") }
        )
    },
    @{
        Name = "竞争策略"
        Widths = @(16, 38, 42, 48, 12)
        Merge = ""
        Filter = "A1:E6"
        Rows = @(
            @{ Values = @("模块", "洞察", "证据", "PM动作", "优先级"); Styles = @(2,2,2,2,2) },
            @{ Values = @("定位", "{{POSITIONING_INSIGHT}}", "{{POSITIONING_EVIDENCE}}", "{{POSITIONING_ACTION}}", "P0") },
            @{ Values = @("产品", "{{PRODUCT_INSIGHT}}", "{{PRODUCT_EVIDENCE}}", "{{PRODUCT_ACTION}}", "P0") },
            @{ Values = @("广告", "{{ADS_INSIGHT}}", "{{ADS_EVIDENCE}}", "{{ADS_ACTION}}", "P1") }
        )
    },
    @{
        Name = "数据来源"
        Widths = @(24, 52, 52)
        Merge = ""
        Filter = "A1:C6"
        Rows = @(
            @{ Values = @("数据来源", "文件/接口", "用途"); Styles = @(2,2,2) },
            @{ Values = @("{{DATA_PROVIDER}}", "asin_detail", "商品基础信息") },
            @{ Values = @("{{DATA_PROVIDER}}", "asin_sales_trend", "销售趋势") },
            @{ Values = @("{{DATA_PROVIDER}}", "traffic_keyword / traffic_extend", "关键词与流量") },
            @{ Values = @("{{DATA_PROVIDER}}", "review", "评论VOC") }
        )
    },
    @{
        Name = "MCP原始数据"
        Widths = @(28, 22, 12, 38, 70, 38)
        Merge = ""
        Filter = "A1:F8"
        Rows = @(
            @{ Values = @("数据文件/接口", "采集时间", "记录序号", "字段路径", "原始值", "备注"); Styles = @(2,2,2,2,2,2) },
            @{ Values = @("{{RAW_SOURCE_1}}", "{{RAW_COLLECTED_AT_1}}", "{{RAW_INDEX_1}}", "{{RAW_FIELD_PATH_1}}", "{{RAW_VALUE_1}}", "{{RAW_NOTE_1}}") },
            @{ Values = @("{{RAW_SOURCE_2}}", "{{RAW_COLLECTED_AT_2}}", "{{RAW_INDEX_2}}", "{{RAW_FIELD_PATH_2}}", "{{RAW_VALUE_2}}", "{{RAW_NOTE_2}}") },
            @{ Values = @("{{RAW_SOURCE_3}}", "{{RAW_COLLECTED_AT_3}}", "{{RAW_INDEX_3}}", "{{RAW_FIELD_PATH_3}}", "{{RAW_VALUE_3}}", "{{RAW_NOTE_3}}") }
        )
    }
)

$tmp = Join-Path $env:TEMP ("amazon_template_" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "_rels") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "xl\_rels") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tmp "xl\worksheets") | Out-Null

SaveText (Join-Path $tmp "[Content_Types].xml") @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet4.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet5.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet6.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet7.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet8.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"@

SaveText (Join-Path $tmp "_rels\.rels") @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"@

$sheetXml = New-Object System.Collections.Generic.List[string]
$relsXml = New-Object System.Collections.Generic.List[string]
for ($i = 0; $i -lt $sheets.Count; $i++) {
    $id = $i + 1
    $sheetXml.Add("<sheet name=`"$($sheets[$i].Name)`" sheetId=`"$id`" r:id=`"rId$id`"/>")
    $relsXml.Add("<Relationship Id=`"rId$id`" Type=`"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet`" Target=`"worksheets/sheet$id.xml`"/>")
    SaveText (Join-Path $tmp "xl\worksheets\sheet$id.xml") (SheetXml $sheets[$i].Rows $sheets[$i].Widths 1 $sheets[$i].Filter $sheets[$i].Merge)
}
$stylesRelId = "rId$($sheets.Count + 1)"

SaveText (Join-Path $tmp "xl\workbook.xml") @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <bookViews><workbookView activeTab="0"/></bookViews>
  <sheets>$($sheetXml -join '')</sheets>
</workbook>
"@

SaveText (Join-Path $tmp "xl\_rels\workbook.xml.rels") @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  $($relsXml -join '')
  <Relationship Id="$stylesRelId" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"@

SaveText (Join-Path $tmp "xl\styles.xml") @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="3"><font><sz val="10"/><name val="Microsoft YaHei"/></font><font><b/><sz val="16"/><color rgb="FFFFFFFF"/><name val="Microsoft YaHei"/></font><font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Microsoft YaHei"/></font></fonts>
  <fills count="4"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF1F4E78"/><bgColor indexed="64"/></patternFill></fill><fill><patternFill patternType="solid"><fgColor rgb="FF5B9BD5"/><bgColor indexed="64"/></patternFill></fill></fills>
  <borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border><border><left style="thin"><color rgb="FFD9E2F3"/></left><right style="thin"><color rgb="FFD9E2F3"/></right><top style="thin"><color rgb="FFD9E2F3"/></top><bottom style="thin"><color rgb="FFD9E2F3"/></bottom><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf><xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFill="1" applyFont="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf><xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFill="1" applyFont="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf></cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>
"@

$resolvedOut = Join-Path (Resolve-Path (Split-Path $OutputPath -Parent)).Path (Split-Path $OutputPath -Leaf)
$zipPath = Join-Path $env:TEMP ("amazon_template_" + [Guid]::NewGuid().ToString("N") + ".zip")
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
$zip = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    Get-ChildItem -Path $tmp -Recurse -File | ForEach-Object {
        $entryName = $_.FullName.Substring($tmp.Length + 1).Replace("\", "/")
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $entryName, [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
}
finally {
    $zip.Dispose()
}

if (Test-Path $resolvedOut) { Remove-Item $resolvedOut -Force }
Move-Item $zipPath $resolvedOut
Remove-Item $tmp -Recurse -Force
Write-Host "Created $resolvedOut"
