<#
  Install.ps1 - installs the OOT keyboard + mouse mod into Lichii. INSTALL.bat runs it.

  What it does
    1. Finds Lichii's data folder (the one with config\qt-config.ini): %APPDATA%\lichii, or asks you.
    2. Copies the mod into it: load\0400486024DEC000\..., the settings file, Apply-Settings, OoT-MouseCapture.exe.
       Your own OoT-Keyboard-Mouse-Settings.ini is kept if you already have one.
    3. Moves other button-icon mods (ButtonPrompts-PlayStation, -Xbox, ...) to mod-backups\ (only one can work).
    4. Runs Apply-Settings.ps1 there, which sets up Player 1 for keyboard and mouse.

  Options (for testing): -Target <folder>  install there without asking
                         -Force            do not stop when Lichii looks like it is running
#>
[CmdletBinding()]
param(
    [string]$Target = '',
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
# Windows PowerShell 5.1 can leave $PSScriptRoot empty, so find our own folder the safe way.
$here = $PSScriptRoot
if (-not $here) { $here = Split-Path -Parent $MyInvocation.MyCommand.Definition }
$titleId = '0400486024DEC000'

function Say([string]$text, [string]$color = 'Gray') { Write-Host $text -ForegroundColor $color }
function Stop-Install([string[]]$lines) {
    Say ''
    foreach ($l in $lines) { Say ('  ' + $l) 'Red' }
    Say ''
    exit 1
}
function Test-DataFolder([string]$p) { return $p -and (Test-Path -LiteralPath (Join-Path $p 'config\qt-config.ini')) }

Say ''
Say '  OOT keyboard + mouse - installer' 'Cyan'
Say '  ================================' 'Cyan'
Say ''

# ---------------------------------------------------------------- the download must be extracted
$mustHave = @('Apply-Settings.ps1', 'OoT-Keyboard-Mouse-Settings.ini', "load\$titleId\ButtonPrompts-KeyboardMouse")
foreach ($m in $mustHave) {
    if (-not (Test-Path -LiteralPath (Join-Path $here $m))) {
        Stop-Install @("A file of the mod is missing next to INSTALL.bat: $m",
            'Extract the whole zip first (right-click the zip > Extract All), then run INSTALL.bat',
            'from the extracted folder. Running it from inside the zip window does not work.')
    }
}

# ---------------------------------------------------------------- Lichii must be closed
$running = @(Get-Process | Where-Object { $_.ProcessName -match '^(lichii|eden|yuzu|citron|sudachi|suyu|torzu)' })
if ($running.Count -gt 0 -and -not $Force) {
    Stop-Install @("Lichii is open ($($running[0].ProcessName).exe). Close it completely, then run INSTALL.bat again.",
        '(Lichii saves its settings when it closes, which would undo the installation.)')
}

# ---------------------------------------------------------------- find the data folder
if ($Target) {
    if ((Test-Path -LiteralPath (Join-Path $Target 'user\config\qt-config.ini')) -and -not (Test-DataFolder $Target)) {
        $Target = Join-Path $Target 'user'
    }
    if (-not (Test-DataFolder $Target)) { Stop-Install @("Not a Lichii data folder (no config\qt-config.ini): $Target") }
} else {
    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($name in @('lichii', 'Lichii', 'fritchii', 'Fritchii')) {
        $p = Join-Path $env:APPDATA $name
        if ((Test-DataFolder $p) -and -not ($candidates -contains $p)) { $candidates.Add($p) }
    }
    if ($candidates.Count -eq 1) {
        $Target = $candidates[0]
        Say ('  Lichii data folder found: ' + $Target)
    } else {
        if ($candidates.Count -gt 1) {
            Say '  More than one Lichii data folder was found:' 'Yellow'
            for ($i = 0; $i -lt $candidates.Count; $i++) { Say ('    ' + ($i + 1) + '. ' + $candidates[$i]) }
            Say ''
        } else {
            Say '  Lichii''s data folder was not found automatically.' 'Yellow'
            Say '  (Portable Lichii keeps it in the "user" folder next to lichii.exe.)'
            Say ''
        }
        Say '  To find it: open Lichii, click File > Open Lichii Folders > Root Data Folder,'
        Say '  click the address bar of the window that opens, copy the address (Ctrl+C), close Lichii,'
        Say '  then paste it here (right-click or Ctrl+V) and press Enter.'
        if ($candidates.Count -gt 1) { Say '  Or type the number of one of the folders above.' }
        Say ''
        for ($try = 0; $try -lt 3 -and -not (Test-DataFolder $Target); $try++) {
            $answer = (Read-Host '  Folder').Trim().Trim('"')
            if ($answer -match '^\d+$' -and [int]$answer -ge 1 -and [int]$answer -le $candidates.Count) {
                $answer = $candidates[[int]$answer - 1]
            }
            if ($answer -and -not (Test-DataFolder $answer) -and (Test-DataFolder (Join-Path $answer 'user'))) {
                $answer = Join-Path $answer 'user'
            }
            if (Test-DataFolder $answer) { $Target = $answer }
            else { Say '  That folder has no config\qt-config.ini, so it is not Lichii''s data folder. Try again.' 'Yellow' }
        }
        if (-not (Test-DataFolder $Target)) {
            Stop-Install @('No Lichii data folder was given.',
                'Start Lichii once and close it (that creates the folder), then run INSTALL.bat again.')
        }
    }
}
$Target = (Resolve-Path -LiteralPath $Target).Path
if ($Target.TrimEnd('\') -eq $here.TrimEnd('\')) {
    Say '  (Already inside the data folder: nothing to copy.)'
}

# ---------------------------------------------------------------- copy the mod
$loadSrc = Join-Path $here "load\$titleId"
$loadDst = Join-Path $Target "load\$titleId"
New-Item -ItemType Directory -Force -Path $loadDst | Out-Null

# Only one ButtonPrompts-* folder can work: move the others aside (nothing is deleted).
$moved = @()
foreach ($d in @(Get-ChildItem -LiteralPath $loadDst -Directory | Where-Object { $_.Name -like 'ButtonPrompts-*' -and $_.Name -ne 'ButtonPrompts-KeyboardMouse' })) {
    $backup = Join-Path $Target 'mod-backups'
    New-Item -ItemType Directory -Force -Path $backup | Out-Null
    $dest = Join-Path $backup $d.Name
    if (Test-Path -LiteralPath $dest) { $dest = $dest + '-' + (Get-Date -Format 'yyyyMMdd-HHmmss') }
    Move-Item -LiteralPath $d.FullName -Destination $dest
    $moved += $d.Name
}

if ($Target.TrimEnd('\') -ne $here.TrimEnd('\')) {
    foreach ($mod in @(Get-ChildItem -LiteralPath $loadSrc -Directory)) {
        $dst = Join-Path $loadDst $mod.Name
        if ($mod.Name -eq 'MouseCamera-Native' -and (Test-Path -LiteralPath $dst)) {
            # keep whether it is on or off: Apply-Settings switches it with mouse_camera
            $on = @(Get-ChildItem -LiteralPath (Join-Path $dst 'exefs') -Filter '*.ips' -ErrorAction SilentlyContinue).Count -gt 0
            Remove-Item -LiteralPath $dst -Recurse -Force
            Copy-Item -LiteralPath $mod.FullName -Destination $dst -Recurse
            if ($on) {
                foreach ($f in @(Get-ChildItem -LiteralPath (Join-Path $dst 'exefs') -Filter '*.ips.off')) {
                    Rename-Item -LiteralPath $f.FullName -NewName ($f.Name -replace '\.off$', '')
                }
            }
        } else {
            if (Test-Path -LiteralPath $dst) { Remove-Item -LiteralPath $dst -Recurse -Force }
            Copy-Item -LiteralPath $mod.FullName -Destination $dst -Recurse
        }
    }
    $profileSrc = Join-Path $here 'config\input\OoT-Keyboard-Mouse.ini'
    if (Test-Path -LiteralPath $profileSrc) {
        New-Item -ItemType Directory -Force -Path (Join-Path $Target 'config\input') | Out-Null
        Copy-Item -LiteralPath $profileSrc -Destination (Join-Path $Target 'config\input') -Force
    }
    foreach ($f in @('Apply-Settings.bat', 'Apply-Settings.ps1', 'OoT-MouseCapture.exe')) {
        if (Test-Path -LiteralPath (Join-Path $here $f)) { Copy-Item -LiteralPath (Join-Path $here $f) -Destination $Target -Force }
    }
    $keep = Join-Path $Target 'OoT-Keyboard-Mouse-Settings.ini'
    if (Test-Path -LiteralPath $keep) {
        Say '  Your OoT-Keyboard-Mouse-Settings.ini was kept (your keys stay as they were).'
        Copy-Item -LiteralPath (Join-Path $here 'OoT-Keyboard-Mouse-Settings.ini') -Destination (Join-Path $Target 'OoT-Keyboard-Mouse-Settings.new.ini') -Force
        Say '  The new version with every option is next to it: OoT-Keyboard-Mouse-Settings.new.ini'
    } else {
        Copy-Item -LiteralPath (Join-Path $here 'OoT-Keyboard-Mouse-Settings.ini') -Destination $keep
    }
}
Say '  Mod files copied.' 'Green'
foreach ($m in $moved) { Say ("  Moved $m to mod-backups (only one button-icon mod can be active).") 'Yellow' }

# ---------------------------------------------------------------- apply the settings
& (Join-Path $Target 'Apply-Settings.ps1') -Root $Target -Force:$Force
exit $LASTEXITCODE
