"""Baut eine Lektions-Seite (Notizblock) im Stil der bisherigen Artifacts.

Nutzung in Python:
    from build import page, task
    html = page(title=..., eyebrow=[...], h1=..., lead=..., note=..., body=..., key=..., label=...)

Die Vorlage (Kopf mit CSS, Skript mit Antwortspeicher und Kopier-Knopf) wird aus der
Chemie-Seite gelesen, damit alle Seiten gleich aussehen.
"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TEMPLATE = os.path.join(ROOT, '04_naturwissenschaften/chemie/uebungen/01_stoffe_teilchen_trennen.html')

EXTRA_CSS = '''
.fig svg .l1 { fill: var(--accent); fill-opacity: .10; stroke: var(--accent); stroke-width: 1; }
.fig svg .l2 { fill: var(--accent); fill-opacity: .25; stroke: var(--accent); stroke-width: 1; }
.fig svg .l3 { fill: var(--accent); fill-opacity: .45; stroke: var(--accent); stroke-width: 1; }
.fig svg .crust { fill: none; stroke: var(--margin); stroke-width: 4; }
.fig svg .green { fill: var(--ok); fill-opacity: .55; stroke: var(--ok); stroke-width: 1; }
.fig svg .org { fill: var(--warn); fill-opacity: .35; stroke: var(--warn); stroke-width: 1; }
.fig svg .wall { fill: none; stroke: var(--ok); stroke-width: 5; }
.fig svg .mem { fill: var(--field); stroke: var(--ink); stroke-width: 1.4; }
.fig svg .vac { fill: var(--accent); fill-opacity: .12; stroke: var(--accent); stroke-width: 1; }
.fig svg .nuc { fill: var(--margin); fill-opacity: .18; stroke: var(--margin); stroke-width: 1.2; }
.yt { font-size: 15px; color: var(--muted); }
'''


def _template():
    src = open(TEMPLATE, encoding='utf-8').read()
    head = src[:src.index('<main class="page">')]
    head = head.replace('</style>', EXTRA_CSS + '</style>', 1)
    script = src[src.index('<script>\n(function () {'):]
    return head, script


def task(n, question, rows=3):
    return f'''    <article class="task">
      <div class="num">{n}</div>
      <div class="body">
        <div class="q">{question}</div>
        <label class="ans" for="ans-{n}">Deine Antwort</label>
        <textarea id="ans-{n}" data-n="{n}" rows="{rows}"></textarea>
      </div>
    </article>
'''


def page(title, eyebrow, h1, lead, note, body, key, label):
    head, script = _template()
    import re
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head, count=1)
    script = re.sub(r"var KEY = '[^']*';", f"var KEY = '{key}';", script, count=1)
    script = re.sub(r"var lines = \['[^']*'\];", f"var lines = ['{label}'];", script, count=1)
    eb = ''.join(f'<span>{e}</span>' for e in eyebrow)
    return f'''{head}<main class="page">
  <header class="top">
    <div class="eyebrow">{eb}</div>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <p class="note">{note}</p>
  </header>
{body}
  <section class="panel" aria-labelledby="send-h">
    <h2 id="send-h">Antworten abgeben</h2>
    <p>Der Knopf kopiert alle Felder als Text. Füg ihn danach im Chat ein. Deine Eingaben bleiben in diesem Browser gespeichert.</p>
    <div class="actions">
      <button type="button" id="copy-btn">Alle Antworten kopieren</button>
      <button type="button" class="ghost" id="clear-btn">Felder leeren</button>
      <span class="status" id="status" role="status"></span>
    </div>
    <textarea id="copy-fallback" hidden readonly aria-label="Antworten zum Kopieren"></textarea>
  </section>

  <section class="panel solutions" aria-labelledby="sol-h">
    <h2 id="sol-h">Lösungen und Erklärungen</h2>
    <p>Kommen hierhin, sobald du mir deine Antworten im Chat geschickt hast.</p>
  </section>
</main>

{script}'''
