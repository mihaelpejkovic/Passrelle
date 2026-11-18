# Logrechner fuer die Passerelle-Vorbereitung
# Start:  powershell -ExecutionPolicy Bypass -File .\logrechner.ps1
# Eingabe wie auf Papier, z. B.  lg(40/3)/lg(5)   log2(8)   log(1.5; 2)   2^-1   sqrt(72)

$ErrorActionPreference = 'Stop'
$inv = [System.Globalization.CultureInfo]::InvariantCulture
$script:last = 0.0
$script:toks = $null
$script:pos = 0

function Show-Hilfe {
    Write-Host ''
    Write-Host 'Rechnen:     +  -  *  /  ^  ( )      Dezimalpunkt: 1.5 (nicht 1,5)'
    Write-Host 'Logarithmen: lg(x)       Zehnerlogarithmus'
    Write-Host '             ln(x)       natuerlicher Logarithmus'
    Write-Host '             log2(x)     Logarithmus zur Basis 2 (log3, log5 ... genauso)'
    Write-Host '             log(b; x)   Logarithmus von x zur Basis b, z. B. log(1.5; 2)'
    Write-Host 'Wurzeln:     sqrt(x)     Quadratwurzel'
    Write-Host '             root(n; x)  n-te Wurzel, z. B. root(3; 27)'
    Write-Host 'Weitere:     abs(x)  exp(x)  sin(x)  cos(x)  tan(x)  (Winkel in Grad)'
    Write-Host 'Konstanten:  pi  e  ans (letztes Ergebnis)'
    Write-Host 'Befehle:     hilfe   q (beenden)'
    Write-Host ''
}

function Get-Tokens([string]$s) {
    $list = New-Object System.Collections.Generic.List[object]
    $i = 0
    while ($i -lt $s.Length) {
        $c = $s[$i]
        if ([char]::IsWhiteSpace($c)) { $i++; continue }
        if ([char]::IsDigit($c) -or $c -eq '.') {
            $j = $i
            while ($j -lt $s.Length -and ([char]::IsDigit($s[$j]) -or $s[$j] -eq '.')) { $j++ }
            $text = $s.Substring($i, $j - $i)
            $num = 0.0
            if (-not [double]::TryParse($text, [System.Globalization.NumberStyles]::Float, $inv, [ref]$num)) {
                throw "Zahl nicht lesbar: '$text'"
            }
            $list.Add(@{ t = 'num'; v = $num })
            $i = $j; continue
        }
        if ([char]::IsLetter($c)) {
            $j = $i
            while ($j -lt $s.Length -and [char]::IsLetterOrDigit($s[$j])) { $j++ }
            $list.Add(@{ t = 'id'; v = $s.Substring($i, $j - $i).ToLower() })
            $i = $j; continue
        }
        if ('+-*/^(),;'.Contains([string]$c)) {
            $list.Add(@{ t = 'op'; v = [string]$c })
            $i++; continue
        }
        throw "Unbekanntes Zeichen: '$c'"
    }
    return ,$list
}

function Peek-Token {
    if ($script:pos -lt $script:toks.Count) { return $script:toks[$script:pos] }
    return $null
}

function Read-Token {
    $t = Peek-Token
    $script:pos++
    return $t
}

function Test-Op($t, [string[]]$ops) {
    return ($null -ne $t -and $t.t -eq 'op' -and $ops -contains $t.v)
}

function Expect-Op([string]$v) {
    $t = Read-Token
    if (-not (Test-Op $t @($v))) { throw "Hier fehlt '$v'" }
}

function Parse-Expr {
    $v = Parse-Term
    while (Test-Op (Peek-Token) @('+', '-')) {
        $op = (Read-Token).v
        $r = Parse-Term
        if ($op -eq '+') { $v = $v + $r } else { $v = $v - $r }
    }
    return $v
}

function Parse-Term {
    $v = Parse-Unary
    while (Test-Op (Peek-Token) @('*', '/')) {
        $op = (Read-Token).v
        $r = Parse-Unary
        if ($op -eq '*') { $v = $v * $r }
        else {
            if ($r -eq 0) { throw 'Division durch 0' }
            $v = $v / $r
        }
    }
    return $v
}

# Minus vor einer Potenz wirkt wie in der Mathematik: -2^2 = -4
function Parse-Unary {
    if (Test-Op (Peek-Token) @('-')) { [void](Read-Token); $v = Parse-Unary; return (-1 * $v) }
    if (Test-Op (Peek-Token) @('+')) { [void](Read-Token); return (Parse-Unary) }
    return (Parse-Power)
}

function Parse-Power {
    $b = Parse-Primary
    if (Test-Op (Peek-Token) @('^')) {
        [void](Read-Token)
        $e = Parse-Unary
        $v = [math]::Pow($b, $e)
        if ([double]::IsNaN($v)) { throw 'Potenz nicht definiert (negative Basis mit Bruch-Exponent?)' }
        return $v
    }
    return $b
}

function Parse-Args {
    Expect-Op '('
    $a = @()
    $a += Parse-Expr
    while (Test-Op (Peek-Token) @(';', ',')) {
        [void](Read-Token)
        $a += Parse-Expr
    }
    Expect-Op ')'
    return ,$a
}

function Get-Log([double]$base, [double]$x) {
    if ($x -le 0) { throw 'Logarithmus gibt es nur von Zahlen groesser 0' }
    if ($base -le 0 -or $base -eq 1) { throw 'Basis muss groesser 0 und ungleich 1 sein' }
    return [math]::Log10($x) / [math]::Log10($base)
}

function Assert-Count([string]$name, $a, [int]$n) {
    if ($a.Count -ne $n) { throw "$name braucht $n Zahl(en), z. B. siehe 'hilfe'" }
}

function Parse-Primary {
    $t = Read-Token
    if ($null -eq $t) { throw 'Ausdruck ist unvollstaendig' }
    if ($t.t -eq 'num') { return $t.v }
    if (Test-Op $t @('(')) {
        $v = Parse-Expr
        Expect-Op ')'
        return $v
    }
    if ($t.t -eq 'id') {
        $name = $t.v
        if ($name -eq 'pi') { return [math]::PI }
        if ($name -eq 'e') { return [math]::E }
        if ($name -eq 'ans') { return $script:last }

        if (-not (Test-Op (Peek-Token) @('('))) { throw "Nach '$name' fehlt eine Klammer, z. B. $name(8)" }
        $a = Parse-Args

        if ($name -match '^log(\d+)$') {
            Assert-Count $name $a 1
            return (Get-Log ([double]$Matches[1]) $a[0])
        }
        switch ($name) {
            'lg'   { Assert-Count 'lg' $a 1; return (Get-Log 10 $a[0]) }
            'ln'   { Assert-Count 'ln' $a 1; if ($a[0] -le 0) { throw 'Logarithmus gibt es nur von Zahlen groesser 0' }; return [math]::Log($a[0]) }
            'log'  { Assert-Count 'log' $a 2; return (Get-Log $a[0] $a[1]) }
            'sqrt' { Assert-Count 'sqrt' $a 1; if ($a[0] -lt 0) { throw 'Keine Wurzel aus negativen Zahlen' }; return [math]::Sqrt($a[0]) }
            'root' {
                Assert-Count 'root' $a 2
                $n = $a[0]; $x = $a[1]
                if ($n -eq 0) { throw 'Wurzelexponent darf nicht 0 sein' }
                if ($x -lt 0) {
                    if ([math]::Abs($n % 2) -eq 1) { return -1 * [math]::Pow(-$x, 1 / $n) }
                    throw 'Gerade Wurzel aus negativer Zahl gibt es nicht'
                }
                return [math]::Pow($x, 1 / $n)
            }
            'abs'  { Assert-Count 'abs' $a 1; return [math]::Abs($a[0]) }
            'exp'  { Assert-Count 'exp' $a 1; return [math]::Exp($a[0]) }
            'sin'  { Assert-Count 'sin' $a 1; return [math]::Sin($a[0] * [math]::PI / 180) }
            'cos'  { Assert-Count 'cos' $a 1; return [math]::Cos($a[0] * [math]::PI / 180) }
            'tan'  { Assert-Count 'tan' $a 1; return [math]::Tan($a[0] * [math]::PI / 180) }
        }
        throw "Unbekannte Funktion: '$name' (siehe 'hilfe')"
    }
    throw "Unerwartetes Zeichen: '$($t.v)'"
}

function Invoke-Rechnung([string]$line) {
    $script:toks = Get-Tokens $line
    $script:pos = 0
    $v = Parse-Expr
    if ($script:pos -lt $script:toks.Count) {
        $rest = $script:toks[$script:pos].v
        if ($rest -eq ',') { throw 'Benutze den Punkt als Dezimaltrennzeichen: 1.5 statt 1,5' }
        throw "Unerwartetes Zeichen: '$rest'"
    }
    if ([double]::IsNaN($v) -or [double]::IsInfinity($v)) { throw 'Ergebnis ist nicht definiert' }
    return $v
}

Write-Host 'Logrechner. Eingabe z. B. lg(40/3)/lg(5)  -  hilfe fuer alle Funktionen, q zum Beenden' -ForegroundColor Cyan
while ($true) {
    $line = Read-Host '>'
    if ($null -eq $line) { break }
    $line = $line.Trim()
    if ($line -eq '') { continue }
    if (@('q', 'quit', 'exit') -contains $line.ToLower()) { break }
    if (@('hilfe', 'help', '?') -contains $line.ToLower()) { Show-Hilfe; continue }
    try {
        $v = Invoke-Rechnung $line
        $script:last = $v
        Write-Host ('= ' + $v.ToString('G12', $inv)) -ForegroundColor Green -NoNewline
        Write-Host ('    gerundet: ' + [math]::Round($v, 3).ToString('0.000', $inv)) -ForegroundColor DarkGray
    }
    catch {
        Write-Host ('Fehler: ' + $_.Exception.Message) -ForegroundColor Red
    }
}
