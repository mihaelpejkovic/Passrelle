# 01 – Lineare und quadratische Gleichungen (Einstieg)

## Worum geht es
Eine Gleichung ist eine Aussage mit einer Unbekannten x. Lösen heisst: alle x finden, für die sie stimmt.
- Linear: x kommt nur "einfach" vor → `ax + b = 0` → genau eine Lösung (ausser Sonderfälle).
- Quadratisch: x² kommt vor → `ax² + bx + c = 0` → 0, 1 oder 2 Lösungen.

## Wozu / wo gebraucht
Nullstellen und Schnittpunkte von Funktionen, Extremwertaufgaben, Vektorgeometrie (Schnitt Gerade–Kugel),
Physik (Wurf: `s = v0·t − ½·g·t²`), Textaufgaben (Flächen, Zins, Geschwindigkeit).

## Wie es funktioniert
**Linear:** Klammern auflösen → x-Terme auf eine Seite, Zahlen auf die andere → durch den Faktor vor x teilen.
Auf beiden Seiten immer dasselbe tun.

**Quadratisch:** zuerst alles auf eine Seite: `ax² + bx + c = 0`. Dann:
- Kein c (`ax² + bx = 0`): x ausklammern → `x(ax + b) = 0` → x = 0 oder x = −b/a.
- Kein b (`ax² + c = 0`): nach x² auflösen, Wurzel ziehen, ± nicht vergessen.
- Sonst Lösungsformel: `x = (−b ± √D) / (2a)` mit Diskriminante `D = b² − 4ac`.
  - D > 0: zwei Lösungen · D = 0: eine Lösung · D < 0: keine reelle Lösung
- Schneller, wenn es aufgeht: faktorisieren. `x² + px + q = (x − x1)(x − x2)` mit `x1 + x2 = −p`, `x1·x2 = q` (Vieta).

## Beispiele

**1) `3(x − 2) = 5x + 4`**
1. Klammer auflösen: `3x − 6 = 5x + 4`
2. x nach links, Zahlen nach rechts: `3x − 5x = 4 + 6` → `−2x = 10`
3. Durch −2: `x = −5`
4. Probe: links 3·(−7) = −21, rechts −25 + 4 = −21 ✓

**2) `2x² − 4x − 6 = 0`**
1. a = 2, b = −4, c = −6
2. D = (−4)² − 4·2·(−6) = 16 + 48 = 64 → zwei Lösungen
3. x = (4 ± 8) / 4 → x1 = 3, x2 = −1
4. Probe x = 3: 18 − 12 − 6 = 0 ✓

**3) `(x + 1)² = 3x + 7`**
1. Ausmultiplizieren: `x² + 2x + 1 = 3x + 7`
2. Alles nach links: `x² − x − 6 = 0`
3. Faktorisieren: zwei Zahlen mit Produkt −6 und Summe −1 → −3 und 2 → `(x − 3)(x + 2) = 0`
4. Ein Produkt ist 0, wenn ein Faktor 0 ist: x1 = 3, x2 = −2
5. Probe x = 3: 16 = 16 ✓ · x = −2: 1 = 1 ✓

## Checkliste
- [ ] Linear oder quadratisch? (Gibt es nach dem Vereinfachen noch ein x²?)
- [ ] Klammern aufgelöst, Brüche weg (mit dem Nenner multiplizieren)
- [ ] Quadratisch: alles auf einer Seite, rechts steht 0
- [ ] a, b, c mit Vorzeichen abgelesen
- [ ] Sonderfall geprüft (ausklammern / Wurzel ziehen / faktorisieren), sonst Lösungsformel
- [ ] D angeschaut: wie viele Lösungen?
- [ ] ± nicht vergessen
- [ ] Probe in der **ursprünglichen** Gleichung

## Aufgaben (ohne Lösungen)
1. `4(2x − 1) − 3(x + 2) = 2x + 5`
2. `x² − 7x + 10 = 0`
3. `3x² + 5x − 2 = 0`
4. Wie viele Lösungen haben `x² − 6x + 9 = 0` und `x² + 2x + 5 = 0`? Begründe mit D.
5. Ein Rechteck hat den Umfang 34 cm und die Fläche 60 cm². Wie lang sind die Seiten?
