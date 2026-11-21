# Passerelle-Vorbereitung: Regeln für Agenten

Dieses Repo ist der Lernarbeitsplatz für die **Ergänzungsprüfung Passerelle, Wintersession 2027** (Selbststudium).
Es wird über viele Chats und Agenten hinweg genutzt. Lies diese Datei und **`FORTSCHRITT.md`** zu Beginn jeder Session.

## Pflicht in jeder Session

1. **Zuerst lesen:** `CLAUDE.md` (diese Datei) und `FORTSCHRITT.md` (aktueller Stand, Log, offene Punkte).
2. **Zeit erfassen:** Beim Start und bei jeder neuen Nachricht des Users `TZ=Europe/Zurich date` ausführen.
   Nachrichtenzeiten sind sonst nicht sichtbar. Lernzeit daraus und aus den Commit-Zeiten schätzen
   (`TZ=Europe/Zurich git log --date=format-local:'%a %d.%m. %H:%M' --format='%ad %s'`).
3. **Nach jedem Lernschritt `FORTSCHRITT.md` aktualisieren:** Session-Log (Datum, Zeitfenster, Dauer, Inhalt,
   Resultate), Stand pro Fach, offene Punkte, Abweichung zum Wochenplan.
4. **Committen und pushen** nach jedem Schritt (Branch gemäss Session-Vorgabe).
5. Dem User nie behaupten, etwas sei erledigt, wenn es nicht geprüft ist. Unsicheres als unsicher markieren.

## Der User

- Berufsmaturität (BMS) vorhanden, Passerelle noch nicht. Selbständig im Bereich KI, darum wenig Zeit unter der Woche.
- Gut in Mathe. Am meisten Arbeit: Naturwissenschaften, dann Mathe, dann Geschichte/Geografie, dann Sprachen.
- Lernt **allein**, ohne Vorbereitungsschule.
- Ziel: Passerelle so schnell wie möglich, danach Fernstudium B.Sc. Informatik (FernUniversität Hagen), dann Master KI/ML.
  Studienstart Oktober 2027 geht nur mit bestandener **ganzer** Prüfung im Winter 2027.
- Entscheid vom 19.11.2026: **ganze Prüfung im Winter 2027, zweite Sprache Englisch.** „Nicht bestehen ist keine Option.“
- Sonntags ab ca. 12 Uhr frei, darum Sonntag mehr Lernstunden.
- **Englisch (Entscheid 21.11.):** User arbeitet auf Englisch, darum Englisch erst gegen Schluss.
  Im Wochenplan bleiben die Englisch-Slots stehen, gelten aber als **Puffer** zum Nachholen anderer Fächer.
- YouTube-Videos als Einstieg sind ok (v. a. Geschichte), danach Notizblock und Aufgaben.

## Prüfungsfakten (geprüft, Quellen in `00_admin/offizielle_dokumente/`)

| Was | Wann / Wie |
|---|---|
| Anmeldung | online bis **1.12.2026, 24:00**; Dossier per A-Post bis erster Werktag danach |
| Gebühr | CHF 700 (200 Anmeldung + 500 Gesamtprüfung) |
| Schriftlich | **15.–19.2.2027, Zürich** (Tage laut Recherche, genau im Aufgebot) |
| Mündlich | **8.–11.3.2027, Pfäffikon SZ** (Deutsch, Englisch, Mathematik) |
| Fächer | Deutsch 4 h + mündlich · Englisch 3 h + mündlich · Mathe 3 h + mündlich · Naturwissenschaften 3 × 80 min (Bio, Chemie, Physik) · Geschichte + Geografie 2 × 2 h |
| Bestehen | Summe der 5 Fachnoten ≥ 20, höchstens 2 unter 4, keine unter 2 |
| Wiederholung | 1 Wiederholung; Fächer mit Note ≥ 5,0 bleiben |
| Hilfsmittel | Rechner **nur** Casio FX-82 Solar/Solar II oder TI-30 ECO RS; eine Formelsammlung (z. B. Fundamentum) ohne Notizen, in NW **nur im Physikteil**; Chemie: offizielles PSE-Blatt |
| Deutsch-Werke Winter 2027 | Bühler *Verschiebung im Gestein* · Dürrenmatt *Der Besuch der alten Dame* · Storm *Der Schimmelreiter* · Burkart, 10 Gedichte (alle vorbereiten) |
| Englisch | 3 Werke von 3 Autoren aus der Liste (Vorschlag: *Animal Farm*, *Of Mice and Men*, *The Old Man and the Sea*; Wahl offen) |
| Regionalgeografie | Winter 2027: **USA** |

Die **Richtlinien 2023** (offizielle Themenlisten) liegen noch nicht im Repo; `sbfi.admin.ch` ist aus der Cloud-Session
nicht erreichbar. Alle `topics.md` sind Entwürfe. Wenn der User das PDF hochlädt: ablegen und Themenlisten abgleichen.
Offizielle alte Prüfungen gibt es nur auf Anfrage beim SBFI (ohne Lösungen).

## Lehrformat (vom User festgelegt)

- **Sprache:** Deutsch (Prüfung ist auf Deutsch). Englisch nur im Fach Englisch.
- **Neues Thema:** kurz und knapp: worum es geht, wozu, wo es gebraucht wird, wie es funktioniert →
  2–3 Beispiele Schritt für Schritt → Checkliste (so kurz wie möglich) → Aufgaben **ohne Lösungen**.
  Ziel: Thema anschneiden und verstehen, Tiefe kommt später.
- **Darstellung:** Übungen und Lektionen als **Artifact „Notizblock“** (HTML auf Häuschenpapier), nicht nur im Chat.
  Vorlage: `03_mathematik/uebungen/gleichungen_test_3.html` (Antwortfelder mit localStorage, Kopier-Knopf,
  Lösungsteil mit Chips richtig/teilweise/falsch, „Deine Antwort“, Schritte, „Merke“-Box, SVG-Grafiken).
  Mathe-Formeln mit MathJax (jsdelivr, `mathjax@3.2.2/es5/tex-svg.js`).
- **Lösungen erst, wenn der User seine Antworten geschickt hat.** Dann auf derselben Seite ergänzen und neu publizieren,
  im Chat nur Bilanz und Hauptfehler.
- **Knacknüsse:** Der User will anspruchsvolle Aufgaben im Prüfungsstil, gemischte Serien ohne Typ-Angabe.
- **Alle Lösungen vor dem Publizieren nachrechnen** (z. B. mit Python).
- **Formelblätter als PDF** pro Fach/Thema (Vorlage: `03_mathematik/notizen/formelblatt_quelle.html`,
  Build: `npm install katex@0.16.11` im Build-Ordner, dann `node tools/pdf/make.js <html> <pdf>` mit Playwright).
- **Lektionen bauen:** `tools/lesson/build.py` (`page()`, `task()`) erzeugt neue Notizblock-Seiten im gleichen Stil.
- **Planung:** Der Wochenplan gibt pro Tag Fach, Thema und Stunden vor; **wann** am Tag, entscheidet der User.
  Generator: `tools/wochenplan/gen.py` (+ `plan.css`), Ausgabe `Wochenplan_Passerelle.pdf`.
  Bei Neuplanung: ab aktuellem Datum mit erledigtem Stand neu rechnen.

## Bekannte Fehlermuster des Users (weiter trainieren)

- Vorzeichen bei `−4ac`, wenn c negativ ist; Vorzeichen beim Rüberbringen von Termen.
- `±` beim Wurzelziehen vergessen (x² = 9); Lösungsfälle vergessen (Parameter a = 0, zweiter Vieta-Fall).
- Durch einen Term mit x (oder lg x) geteilt → Lösung verloren. Stattdessen ausklammern.
- Exponenten bei Produkten multipliziert statt addiert; Exponenten bei Summen verglichen.
- Basiswechsel verkehrt herum (Basis gehört in den Nenner); Betrag: ± auf das Ergebnis statt auf den Inhalt.

## Repo-Struktur

```
CLAUDE.md / AGENTS.md     Regeln für Agenten (AGENTS.md verweist hierher)
FORTSCHRITT.md            Stand, Session-Log, Lernzeit, offene Punkte  ← immer aktuell halten
README.md                 Prüfungsüberblick
STUDY_PLAN.md             Entscheid, Wochenbudget
THEMEN_UND_AUFWAND.md     alle Themen mit Stundenschätzung
Wochenplan_Passerelle.pdf Tagesplan bis zur Prüfung (1 Seite = 1 Woche)
00_admin/                 Anmeldung, offizielle PDFs
01_deutsch/ 02_englisch/ 03_mathematik/ 04_naturwissenschaften/{biologie,chemie,physik}/
05_geistes_sozialwissenschaften/{geschichte,geografie}/
    je: topics.md, notizen/, uebungen/, alte_pruefungen/
tools/                    logrechner.ps1, pdf/make.js, wochenplan/
```

## Publizierte Artifacts (zum Aktualisieren per URL)

| Seite | Datei | URL |
|---|---|---|
| Mathe Knacknüsse Serie 1 | `03_mathematik/uebungen/knacknuesse_gleichungen.html` | https://claude.ai/artifact/9RF9wR26nk9geuQt9QYHbF |
| Mathe gemischt Serie 2 | `03_mathematik/uebungen/gleichungen_gemischt_2.html` | https://claude.ai/artifact/HuXmB8seLtNLhesHBu9J1j |
| Mathe Abschlusstest Gleichungen | `03_mathematik/uebungen/gleichungen_test_3.html` | https://claude.ai/artifact/Aqscedwc9xgjbXeStmiWAo |
| Chemie 1: Stoffe, Teilchenmodell, Trennverfahren | `04_naturwissenschaften/chemie/uebungen/01_stoffe_teilchen_trennen.html` | https://claude.ai/artifact/ViVbzcZMYw3Erc3StJdKR3 |
| Biologie 1: Zellbau (Teil 1 von 3) | `04_naturwissenschaften/biologie/uebungen/01_zellbiologie_zellbau.html` | https://claude.ai/artifact/Byv8uU5Lt23GE8Y9Kpi9cj |
| Geschichte 1: Aufklärung, Revolution, Napoleon | `05_geistes_sozialwissenschaften/geschichte/uebungen/01_aufklaerung_revolution_napoleon.html` | https://claude.ai/artifact/YVXPaCaBCWDQFPZcWoMo1y |
| Physik 1: Grössen, Einheiten, Messen | `04_naturwissenschaften/physik/uebungen/01_groessen_einheiten.html` | https://claude.ai/artifact/3wYzsU9B49Exx3WMSHbcyT |
| Geografie 1: Erdaufbau, Plattentektonik (Teil 1 von 2) | `05_geistes_sozialwissenschaften/geografie/uebungen/01_geologie_plattentektonik.html` | https://claude.ai/artifact/AAMC6CuLqiUnz9cKe97j8u |

Neue Artifacts hier und in `FORTSCHRITT.md` eintragen.
