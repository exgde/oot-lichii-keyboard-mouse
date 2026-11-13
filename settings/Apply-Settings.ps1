<#
  Apply-Settings.ps1 - copies OoT-Keyboard-Mouse-Settings.ini into Lichii.

  Normal use: close Lichii, then double-click Apply-Settings.bat (it runs this script).

  What it does
    1. Reads OoT-Keyboard-Mouse-Settings.ini (next to this script).
    2. Writes the Lichii input profile  config\input\OoT-Keyboard-Mouse.ini.
    3. Writes the same keys and the mouse values straight into config\qt-config.ini
       (Player 1), after saving a copy as config\qt-config.ini.pre-keyboard-mouse.
    4. mouse_camera = native: switches on the game patch in load\0400486024DEC000\MouseCamera-Native
       (with your speed and invert written into it) and the real mouse (mouse_enabled).
       mouse_camera = stick: switches that patch off again.
    Nothing is written if the settings file has a mistake.

  Options (for testing): -Root <folder>   Lichii data folder (default: the folder of this script)
                         -Settings <file> settings file (default: next to this script)
                         -DryRun          show what would change, write nothing
                         -Force           do not stop when Lichii looks like it is running
#>
[CmdletBinding()]
param(
    [string]$Root = '',
    [string]$Settings = '',
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
# Windows PowerShell 5.1 leaves $PSScriptRoot empty in param() defaults, so find the script folder here.
if (-not $Root) { $Root = $PSScriptRoot }
if (-not $Root) { $Root = Split-Path -Parent $MyInvocation.MyCommand.Definition }
if (-not $Root) { $Root = (Get-Location).Path }
$inv = [Globalization.CultureInfo]::InvariantCulture
if (-not $Settings) { $Settings = Join-Path $Root 'OoT-Keyboard-Mouse-Settings.ini' }

# ---------------------------------------------------------------- is this the Lichii data folder?
# It is the folder that holds config\qt-config.ini. Portable Lichii keeps it in a "user" folder next to lichii.exe,
# so files copied next to lichii.exe still work.
if (-not (Test-Path -LiteralPath (Join-Path $Root 'config\qt-config.ini')) -and
    (Test-Path -LiteralPath (Join-Path $Root 'user\config\qt-config.ini'))) {
    $Root = Join-Path $Root 'user'
}
if (-not (Test-Path -LiteralPath (Join-Path $Root 'config\qt-config.ini')) -and -not $DryRun) {
    $appdata = Join-Path $env:APPDATA 'lichii'
    Write-Host ''
    Write-Host '  These files are not in the Lichii data folder yet.' -ForegroundColor Red
    Write-Host ('  This folder: ' + $Root)
    Write-Host ''
    Write-Host '  How to find the right folder:' -ForegroundColor Cyan
    Write-Host '    1. Open Lichii (no game needed).'
    Write-Host '    2. Click File > Open Lichii Folders > Root Data Folder.'
    Write-Host '       A folder opens that has "config", "load" and "nand" inside.'
    if (Test-Path -LiteralPath (Join-Path $appdata 'config\qt-config.ini')) {
        Write-Host ('       On this PC it is most likely: ' + $appdata) -ForegroundColor Yellow
    }
    Write-Host '    3. Close Lichii.'
    Write-Host '    4. Copy everything from the download into that folder (say Yes to replace).'
    Write-Host '    5. Double-click Apply-Settings.bat there.'
    Write-Host ''
    Write-Host '  Never started Lichii on this PC? Start it once and close it: it creates the folder.'
    Write-Host ''
    exit 1
}

function Fail([string[]]$messages) {
    Write-Host ''
    foreach ($m in $messages) { Write-Host ("  ERROR: " + $m) -ForegroundColor Red }
    Write-Host ''
    exit 1
}

# ---------------------------------------------------------------- key tables
$keyCodes = @{}
foreach ($c in [char[]]'abcdefghijklmnopqrstuvwxyz') { $keyCodes[[string]$c] = [int][char]::ToUpper($c) }
foreach ($c in [char[]]'0123456789') { $keyCodes[[string]$c] = [int]$c }
$named = @{
    'space' = 32; 'enter' = 16777220; 'return' = 16777220; 'tab' = 16777217; 'backspace' = 16777219
    'esc' = 16777216; 'escape' = 16777216; 'insert' = 16777222; 'delete' = 16777223
    'home' = 16777232; 'end' = 16777233; 'left' = 16777234; 'up' = 16777235; 'right' = 16777236; 'down' = 16777237
    'pageup' = 16777238; 'pagedown' = 16777239; 'shift' = 16777248; 'ctrl' = 16777249; 'control' = 16777249
    'alt' = 16777251; 'capslock' = 16777252
    'comma' = 44; 'minus' = 45; 'period' = 46; 'slash' = 47; 'semicolon' = 59; 'equals' = 61
    'bracketleft' = 91; 'backslash' = 92; 'bracketright' = 93; 'grave' = 96; 'apostrophe' = 39
}
foreach ($k in $named.Keys) { $keyCodes[$k] = $named[$k] }
for ($i = 1; $i -le 12; $i++) { $keyCodes["f$i"] = 16777263 + $i }
$mouseButtons = @{ 'mouse_left' = 0; 'mouse_right' = 1; 'mouse_middle' = 2; 'mouse_back' = 3; 'mouse_forward' = 4 }

function ConvertTo-Binding([string]$value) {
    $v = $value.Trim().ToLowerInvariant()
    if ($v -eq '' -or $v -eq 'none') { return 'engine:keyboard,code:0,toggle:0' }
    if ($mouseButtons.ContainsKey($v)) { return ('engine:mouse,button:' + $mouseButtons[$v]) }
    if ($keyCodes.ContainsKey($v)) { return ('engine:keyboard,code:' + $keyCodes[$v] + ',toggle:0') }
    if ($v -match '^code:(\d{1,10})$') { return ('engine:keyboard,code:' + $Matches[1] + ',toggle:0') }
    return $null
}

# ---------------------------------------------------------------- settings and defaults
# name -> default value. Order = order in the settings file.
$bindingNames = @('button_y', 'button_a', 'button_b', 'button_x', 'button_zl', 'button_zr', 'button_l', 'button_r',
    'button_r3', 'button_l3', 'button_plus', 'button_minus', 'dpad_up', 'dpad_left', 'dpad_right', 'dpad_down',
    'button_home', 'button_screenshot', 'move_up', 'move_down', 'move_left', 'move_right', 'walk_key')
$defaults = [ordered]@{
    'button_y' = 'mouse_left'; 'button_a' = 'space'; 'button_b' = 'c'; 'button_x' = 'r'
    'button_zl' = 'shift'; 'button_zr' = 'mouse_right'; 'button_l' = 'q'; 'button_r' = 'e'
    'button_r3' = 'mouse_middle'; 'button_l3' = 'none'; 'button_plus' = 'enter'; 'button_minus' = 'tab'
    'dpad_up' = '1'; 'dpad_left' = '2'; 'dpad_right' = '3'; 'dpad_down' = '4'
    'button_home' = 'none'; 'button_screenshot' = 'none'
    'move_up' = 'w'; 'move_down' = 's'; 'move_left' = 'a'; 'move_right' = 'd'; 'walk_key' = 'z'; 'walk_speed' = '0.5'
    'mouse_sens' = '5.0'; 'mouse_sens_x' = ''; 'mouse_sens_y' = ''; 'mouse_invert_y' = 'false'; 'mouse_camera' = 'stick'
    'mouse_deadzone_boost' = '20'; 'mouse_stop_speed' = '18'; 'mouse_min_decay' = '6'; 'hide_cursor' = 'true'
}

if (-not (Test-Path -LiteralPath $Settings)) {
    Fail @("Settings file not found: $Settings", 'Keep OoT-Keyboard-Mouse-Settings.ini in the same folder as Apply-Settings.bat.')
}

$errors = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$given = @{}
$lineNo = 0
foreach ($raw in (Get-Content -LiteralPath $Settings -Encoding UTF8)) {
    $lineNo++
    $line = $raw.Trim()
    if ($line -eq '' -or $line.StartsWith(';') -or $line.StartsWith('#') -or $line.StartsWith('[')) { continue }
    $eq = $line.IndexOf('=')
    if ($eq -lt 1) { $errors.Add("line ${lineNo}: expected  name = value  but found: $raw"); continue }
    $name = $line.Substring(0, $eq).Trim().ToLowerInvariant()
    $value = ($line.Substring($eq + 1) -split ';')[0].Trim()
    if (-not $defaults.Contains($name)) { $errors.Add("line ${lineNo}: unknown setting '$name' (check the spelling)"); continue }
    if ($given.ContainsKey($name)) { $warnings.Add("line ${lineNo}: '$name' is set twice; the last one is used") }
    $given[$name] = [pscustomobject]@{ Value = $value; Line = $lineNo }
}

function Get-Setting([string]$name) {
    if ($given.ContainsKey($name)) { return $given[$name].Value }
    return $defaults[$name]
}
function Get-Line([string]$name) { if ($given.ContainsKey($name)) { return $given[$name].Line } else { return 0 } }

function ConvertTo-Number([string]$text, [double]$min, [double]$max, [string]$name, [bool]$wholeNumber) {
    $t = $text.Trim().Replace(',', '.')
    $d = 0.0
    if (-not [double]::TryParse($t, [Globalization.NumberStyles]::Float, $inv, [ref]$d)) {
        $errors.Add("line $(Get-Line $name): '$name' needs a number, found '$text'"); return $null
    }
    if ($d -lt $min -or $d -gt $max) {
        $errors.Add("line $(Get-Line $name): '$name' must be between $min and $max, found '$text'"); return $null
    }
    if ($wholeNumber -and $d -ne [math]::Floor($d)) {
        $errors.Add("line $(Get-Line $name): '$name' must be a whole number, found '$text'"); return $null
    }
    return $d
}
function ConvertTo-Choice([string]$text, [string[]]$choices, [string]$name) {
    $t = $text.Trim().ToLowerInvariant()
    if ($t -in $choices) { return $t }
    $errors.Add("line $(Get-Line $name): '$name' must be one of: $($choices -join ', '); found '$text'"); return $null
}
function ConvertTo-Bool([string]$text, [string]$name) {
    switch ($text.Trim().ToLowerInvariant()) {
        { $_ -in 'true', 'yes', 'on', '1' } { return $true }
        { $_ -in 'false', 'no', 'off', '0' } { return $false }
        default { $errors.Add("line $(Get-Line $name): '$name' must be true or false, found '$text'"); return $null }
    }
}

# keys and buttons
$bind = @{}
foreach ($name in $bindingNames) {
    $text = Get-Setting $name
    $b = ConvertTo-Binding $text
    if ($null -eq $b) {
        $errors.Add("line $(Get-Line $name): '$text' is not a key or mouse button name (setting '$name'). See the list at the top of the settings file.")
    } else { $bind[$name] = $b }
}
# mouse and movement numbers
$walkSpeed = ConvertTo-Number (Get-Setting 'walk_speed') 0.1 1.0 'walk_speed' $false
$sens = ConvertTo-Number (Get-Setting 'mouse_sens') 0.1 10.0 'mouse_sens' $false
$sensX = $sens; $sensY = $sens
if ((Get-Setting 'mouse_sens_x') -ne '') { $sensX = ConvertTo-Number (Get-Setting 'mouse_sens_x') 0.1 10.0 'mouse_sens_x' $false }
if ((Get-Setting 'mouse_sens_y') -ne '') { $sensY = ConvertTo-Number (Get-Setting 'mouse_sens_y') 0.1 10.0 'mouse_sens_y' $false }
$deadzone = ConvertTo-Number (Get-Setting 'mouse_deadzone_boost') 0 100 'mouse_deadzone_boost' $true
$stopSpeed = ConvertTo-Number (Get-Setting 'mouse_stop_speed') 0 100 'mouse_stop_speed' $true
$minDecay = ConvertTo-Number (Get-Setting 'mouse_min_decay') 0 100 'mouse_min_decay' $true
$invertY = ConvertTo-Bool (Get-Setting 'mouse_invert_y') 'mouse_invert_y'
$hideCursor = ConvertTo-Bool (Get-Setting 'hide_cursor') 'hide_cursor'
$camera = ConvertTo-Choice (Get-Setting 'mouse_camera') @('stick', 'native') 'mouse_camera'
$native = ($camera -eq 'native')

if ($errors.Count -gt 0) {
    Fail (@("The settings file has $($errors.Count) problem(s). Nothing was changed.") + @($errors))
}

# warnings: same key twice, keys Lichii itself uses
$seen = @{}
foreach ($name in $bindingNames) {
    $v = (Get-Setting $name).Trim().ToLowerInvariant()
    if ($v -eq '' -or $v -eq 'none') { continue }
    if ($seen.ContainsKey($v)) { $warnings.Add("'$v' is used for both $($seen[$v]) and $name") } else { $seen[$v] = $name }
    if ($v -in 'ctrl', 'control', 'alt', 'esc', 'escape') {
        $warnings.Add("'$v' (for $name) clashes with Lichii: Ctrl+Q quits, Ctrl+F9 toggles mouse panning, Alt opens the menu bar, Esc leaves fullscreen")
    }
}

# ---------------------------------------------------------------- build the profile
function F6([double]$x) { return [string]::Format($inv, '{0:F6}', $x) }
function Esc([string]$s) { return $s.Replace(':', '$0').Replace(',', '$1') }
$none = 'engine:keyboard,code:0,toggle:0'
$lstick = 'engine:analog_from_button,right:' + (Esc $bind['move_right']) + ',modifier_scale:' + (F6 $walkSpeed) +
    ',up:' + (Esc $bind['move_up']) + ',down:' + (Esc $bind['move_down']) + ',left:' + (Esc $bind['move_left']) +
    ',modifier:' + (Esc $bind['walk_key'])
$rstick = 'engine:mouse,axis_x:0,axis_y:1,threshold:0.500000,range:1.000000,deadzone:0.000000'
if ($invertY) { $rstick += ',invert_y:-' }
if ($native) {
    # The game patch reads the mouse itself. The right stick must not use the mouse: with mouse panning off,
    # Lichii turns "mouse moved while a button is held" into right-stick input (so attacking would move the camera).
    $rstick = 'engine:analog_from_button,up:' + (Esc $none) + ',down:' + (Esc $none) + ',left:' + (Esc $none) + ',right:' + (Esc $none) + ',modifier:' + (Esc $none) + ',modifier_scale:0.500000'
}

$pairs = @(
    @('button_a', $bind['button_a']), @('button_b', $bind['button_b']), @('button_x', $bind['button_x']), @('button_y', $bind['button_y']),
    @('button_lstick', $bind['button_l3']), @('button_rstick', $bind['button_r3']),
    @('button_l', $bind['button_l']), @('button_r', $bind['button_r']), @('button_zl', $bind['button_zl']), @('button_zr', $bind['button_zr']),
    @('button_plus', $bind['button_plus']), @('button_minus', $bind['button_minus']),
    @('button_dleft', $bind['dpad_left']), @('button_dup', $bind['dpad_up']), @('button_dright', $bind['dpad_right']), @('button_ddown', $bind['dpad_down']),
    @('button_slleft', $none), @('button_srleft', $none),
    @('button_home', $bind['button_home']), @('button_screenshot', $bind['button_screenshot']),
    @('button_slright', $none), @('button_srright', $none),
    @('lstick', $lstick), @('rstick', $rstick),
    @('motionleft', $none), @('motionright', $none)
)
$profileName = 'OoT-Keyboard-Mouse'
$sb = New-Object System.Text.StringBuilder
[void]$sb.Append("[Controls]`n")
foreach ($p in $pairs) {
    [void]$sb.Append($p[0] + '\default=false' + "`n")
    [void]$sb.Append($p[0] + '="' + $p[1] + '"' + "`n")
}
$profileText = $sb.ToString()

# ---------------------------------------------------------------- qt-config helpers
function Find-Section([System.Collections.Generic.List[string]]$lines, [string]$section) {
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -eq "[$section]") { $start = $i; break }
    }
    if ($start -lt 0) { return $null }
    $end = $lines.Count
    for ($i = $start + 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i].StartsWith('[')) { $end = $i; break }
    }
    return @($start, $end)
}
function Set-QtValue([System.Collections.Generic.List[string]]$lines, [string]$section, [string]$key, [string]$value, [bool]$isDefault) {
    $range = Find-Section $lines $section
    if ($null -eq $range) { throw "section [$section] not found in qt-config.ini" }
    $defIdx = -1; $valIdx = -1
    for ($i = $range[0] + 1; $i -lt $range[1]; $i++) {
        if ($lines[$i].StartsWith($key + '\default=', [StringComparison]::Ordinal)) { $defIdx = $i }
        elseif ($lines[$i].StartsWith($key + '=', [StringComparison]::Ordinal)) { $valIdx = $i }
    }
    $defLine = $key + '\default=' + $(if ($isDefault) { 'true' } else { 'false' })
    $valLine = $key + '=' + $value
    if ($defIdx -ge 0 -and $valIdx -ge 0) { $lines[$defIdx] = $defLine; $lines[$valIdx] = $valLine }
    elseif ($defIdx -ge 0) { $lines[$defIdx] = $defLine; $lines.Insert($defIdx + 1, $valLine) }
    elseif ($valIdx -ge 0) { $lines[$valIdx] = $valLine; $lines.Insert($valIdx, $defLine) }
    else {
        $at = $range[1]
        while ($at -gt $range[0] + 1 -and $lines[$at - 1].Trim() -eq '') { $at-- }
        $lines.Insert($at, $valLine); $lines.Insert($at, $defLine)
    }
}
function Get-Sens([double]$scale) { return [int][math]::Min(100, [math]::Max(1, [math]::Round($scale * 10, [MidpointRounding]::AwayFromZero))) }

$qtPath = Join-Path $Root 'config\qt-config.ini'
$buildId = 'E0F3CCFAF50065AE4EA01EB5AEB13B1A45DA3348'
$ipsPath = Join-Path $Root ('load\0400486024DEC000\MouseCamera-Native\exefs\' + $buildId + '.ips')
$ipsOff = $ipsPath + '.off'
# Camera speed in native mode: degrees per mouse step. OoT-MouseCapture sets the Windows pointer speed so that one
# step of the mouse is one pixel of the game's 1280x720 picture, so this is degrees per mouse count.
# mouse_sens 5 = 0.06 degrees: about 15 cm of mouse for a full turn at 1600 DPI.
function Get-NativeDegrees([double]$scale) { return $scale * 0.012 }
$profilePath = Join-Path $Root ('config\input\' + $profileName + '.ini')
$utf8 = New-Object System.Text.UTF8Encoding($false)

# ---------------------------------------------------------------- is Lichii running?
$running = @(Get-Process | Where-Object { $_.ProcessName -match '^(lichii|eden|yuzu|citron|sudachi|suyu|torzu)' })
if ($running.Count -gt 0 -and -not $DryRun -and -not $Force) {
    Fail @("Lichii is running ($($running[0].ProcessName).exe). Close it first: it would overwrite these settings when it exits.")
}

if ($native -and -not (Test-Path -LiteralPath $ipsPath) -and -not (Test-Path -LiteralPath $ipsOff)) {
    Fail @('mouse_camera = native needs the game patch, but it is not here:', $ipsPath,
        'Copy the load folder from the download into the Lichii data folder (step 3 of the install), then run this again.')
}

# ---------------------------------------------------------------- do it
Write-Host ''
Write-Host '  OOT keyboard + mouse settings' -ForegroundColor Cyan
Write-Host ('  settings file : ' + $Settings)
Write-Host ('  Lichii folder : ' + $Root)
if ($DryRun) { Write-Host '  (dry run: nothing is written)' -ForegroundColor Yellow }

if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path (Split-Path $profilePath) | Out-Null
    [IO.File]::WriteAllText($profilePath, $profileText, $utf8)
}
Write-Host ('  profile       : ' + $profilePath)

if (Test-Path -LiteralPath $qtPath) {
    $text = [IO.File]::ReadAllText($qtPath, $utf8)
    $eol = if ($text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $list = New-Object 'System.Collections.Generic.List[string]'
    $list.AddRange([string[]]$text.Split([string[]]@("`r`n", "`n"), [StringSplitOptions]::None))

    foreach ($p in $pairs) {
        Set-QtValue $list 'Controls' ('player_0_' + $p[0]) ('"' + $p[1] + '"') $false
    }
    Set-QtValue $list 'Controls' 'player_0_type' '0' $true
    Set-QtValue $list 'Controls' 'player_0_connected' 'true' $true
    Set-QtValue $list 'Controls' 'player_0_profile_name' $profileName $false
    $sx = Get-Sens $sensX; $sy = Get-Sens $sensY
    Set-QtValue $list 'Controls' 'mouse_panning_x_sensitivity' "$sx" ($sx -eq 50)
    Set-QtValue $list 'Controls' 'mouse_panning_y_sensitivity' "$sy" ($sy -eq 50)
    Set-QtValue $list 'Controls' 'mouse_panning_deadzone_counterweight' "$([int]$deadzone)" ([int]$deadzone -eq 20)
    Set-QtValue $list 'Controls' 'mouse_panning_decay_strength' "$([int]$stopSpeed)" ([int]$stopSpeed -eq 18)
    Set-QtValue $list 'Controls' 'mouse_panning_min_decay' "$([int]$minDecay)" ([int]$minDecay -eq 6)
    Set-QtValue $list 'UI' 'hideInactiveMouse' $(if ($hideCursor) { 'true' } else { 'false' }) $hideCursor
    Set-QtValue $list 'Controls' 'mouse_enabled' $(if ($native) { 'true' } else { 'false' }) (-not $native)

    $newText = [string]::Join($eol, $list)
    if ($newText.Length -lt $text.Length * 0.9) { Fail @('Internal check failed: the new qt-config.ini would be much shorter than the old one. Nothing was written.') }
    if (-not $DryRun) {
        $backup = $qtPath + '.pre-keyboard-mouse'
        if (-not (Test-Path -LiteralPath $backup)) { Copy-Item -LiteralPath $qtPath -Destination $backup }
        $tmp = $qtPath + '.tmp'
        [IO.File]::WriteAllText($tmp, $newText, $utf8)
        Move-Item -LiteralPath $tmp -Destination $qtPath -Force
        Write-Host ('  qt-config.ini : updated (copy of the old one: ' + (Split-Path $backup -Leaf) + ')')
    } else {
        Write-Host '  qt-config.ini : would be updated'
    }
} else {
    Write-Host '  qt-config.ini : not found (dry run only checks the settings file).' -ForegroundColor Yellow
}

# ---------------------------------------------------------------- native camera patch
# The patch carries its settings after the marker OOTMCAM1: yaw and pitch in degrees per mouse step
# (a negative pitch inverts up/down).
if ($native) {
    $src = if (Test-Path -LiteralPath $ipsPath) { $ipsPath } else { $ipsOff }
    $bytes = [IO.File]::ReadAllBytes($src)
    $marker = [Text.Encoding]::ASCII.GetBytes('OOTMCAM1')
    $at = -1
    for ($i = 0; $i -le $bytes.Length - 16; $i++) {
        $ok = $true
        for ($j = 0; $j -lt 8; $j++) { if ($bytes[$i + $j] -ne $marker[$j]) { $ok = $false; break } }
        if ($ok) { $at = $i + 8; break }
    }
    if ($at -lt 0) { Fail @("The game patch has no settings block (OOTMCAM1): $src", 'Download the mod again.') }
    $yaw = [single](Get-NativeDegrees $sensX)
    $pitch = [single](Get-NativeDegrees $sensY)
    if ($invertY) { $pitch = [single](-$pitch) }   # keep it a 4-byte float for GetBytes
    [Array]::Copy([BitConverter]::GetBytes($yaw), 0, $bytes, $at, 4)
    [Array]::Copy([BitConverter]::GetBytes($pitch), 0, $bytes, $at + 4, 4)
    if (-not $DryRun) {
        [IO.File]::WriteAllBytes($ipsPath, $bytes)
        if (Test-Path -LiteralPath $ipsOff) { Remove-Item -LiteralPath $ipsOff }
    }
    Write-Host ('  game patch    : ON  ' + $ipsPath)
} elseif (Test-Path -LiteralPath $ipsPath) {
    if (-not $DryRun) { Move-Item -LiteralPath $ipsPath -Destination $ipsOff -Force }
    Write-Host '  game patch    : OFF (MouseCamera-Native renamed to .ips.off)'
}

# ---------------------------------------------------------------- summary
Write-Host ''
Write-Host '  Keys' -ForegroundColor Cyan
foreach ($name in $bindingNames) { Write-Host ('    {0,-18} = {1}' -f $name, (Get-Setting $name)) }
Write-Host ('    {0,-18} = {1}' -f 'walk_speed', (F6 $walkSpeed))
Write-Host '  Mouse' -ForegroundColor Cyan
Write-Host ('    camera speed x/y   = {0} / {1}  (Lichii values {2} / {3})' -f (F6 $sensX), (F6 $sensY), (Get-Sens $sensX), (Get-Sens $sensY))
Write-Host ('    invert up/down     = {0}' -f $invertY)
Write-Host ('    mouse camera       = {0}' -f $camera)
if ($native) { Write-Host ([string]::Format($inv, '    native speed x/y   = {0:F3} / {1:F3} degrees per mouse step', (Get-NativeDegrees $sensX), (Get-NativeDegrees $sensY))) }
Write-Host ('    deadzone boost {0}, stop speed {1}, minimum decay {2}, hide cursor {3}' -f [int]$deadzone, [int]$stopSpeed, [int]$minDecay, $hideCursor)

foreach ($w in $warnings) { Write-Host ('  WARNING: ' + $w) -ForegroundColor Yellow }

$changed = @($bindingNames | Where-Object { (Get-Setting $_).Trim().ToLowerInvariant() -ne $defaults[$_] })
if ($changed.Count -gt 0) {
    Write-Host ''
    Write-Host '  Note: you changed keys. They work, but the key pictures inside the game still show the' -ForegroundColor Yellow
    Write-Host '  default keys (see docs/CONFIGURATION.md on GitHub to redraw them).' -ForegroundColor Yellow
}
Write-Host ''
if ($native) {
    Write-Host '  Done. Each time you play:' -ForegroundColor Green
    Write-Host '    1. Start OoT-MouseCapture.exe (it can stay open).' -ForegroundColor Green
    Write-Host '    2. Start the game in Lichii, click the picture once, press Ctrl+F9 once (the pointer disappears).' -ForegroundColor Green
    Write-Host '    Alt+Tab gives the normal mouse back.' -ForegroundColor Green
} else {
    Write-Host '  Done. Start Lichii. Each time you start the game: click its window, press Ctrl+F9 once.' -ForegroundColor Green
}
Write-Host ''
exit 0
