import datetime as dt, html, json, sys
D = dt.date
ONE = dt.timedelta(1)

# ---------- topic queues (hours of content, incl. exercises) ----------
Q = {
 'MA': [("Gleichungen: Basiswechsel, Schwachstellen",3),("Ungleichungen",4),("Gleichungssysteme",4),
        ("Potenzen, Wurzeln, Logarithmen",3),("Funktionen allgemein",5),("Lineare und quadratische Funktionen",5),
        ("Polynom- und gebrochenrationale Funktionen",6),("Exponential- und Logarithmusfunktionen",5),
        ("Folgen und Reihen",4),("Trigonometrie",10),("Grenzwerte und Stetigkeit",3),("Differentialrechnung",12),
        ("Integralrechnung",10),("Vektorgeometrie",12),("Stochastik",10)],
 'CH': [("Stoffe, Teilchenmodell, Trennverfahren",3),("Atombau, Periodensystem",5),("Bindungen, zwischenmolekulare Kräfte",8),
        ("Reaktionsgleichungen, Stöchiometrie",8),("Energetik, Kinetik, Gleichgewicht",7),("Säuren, Basen, pH",8),
        ("Redox, Elektrochemie",7),("Organische Chemie",10)],
 'BI': [("Zellbiologie",8),("Stoffwechsel: Enzyme, Zellatmung, Fotosynthese",8),("Genetik",12),
        ("Humanbiologie",12),("Ökologie",6),("Evolution",6)],
 'PH': [("Grössen, Einheiten, Messen",2),("Kinematik",8),("Dynamik",8),("Arbeit, Energie, Leistung, Impuls",7),
        ("Elektrizitätslehre",10),("Wärme, Schwingungen, Wellen (laut Richtlinien prüfen)",8)],
 'GE': [("Aufklärung, Franz. Revolution, Napoleon",4),("Industrialisierung, soziale Frage",3),("Nationalismus, Imperialismus",3),
        ("1. Weltkrieg, Russische Revolution",4),("Zwischenkriegszeit, Faschismus, NS",4),("2. Weltkrieg, Holocaust",4),
        ("Kalter Krieg 1945–1991",4),("Dekolonisation",3),("Schweiz: Geschichte und politisches System",6),("Quellenanalyse",3)],
 'GG': [("Geologie, Plattentektonik",5),("Geologie der Schweiz",3),("Geomorphologie",3),("Klima, Wetter, Klimawandel",5),
        ("Bevölkerung, Migration",4),("Stadt, Verstädterung",3),("Raumplanung",2),("Wirtschaft, Globalisierung",4),
        ("Regionalgeografie USA",6),("Karten, Diagramme, Statistiken",2)],
 'DE': [("Epochen und Gattungen",4),("Dürrenmatt: Der Besuch der alten Dame",6),("Storm: Der Schimmelreiter",7),
        ("Bühler: Verschiebung im Gestein",8),("Burkart: 10 Gedichte",5),("Aufsatz: Erörterung, Interpretation",12)],
 'EN': [("Grammatik auffrischen",5),("Werk 1 lesen und erarbeiten",8),("Werk 2 lesen und erarbeiten",8),
        ("Writing: Essay",6),("Werk 3 lesen und erarbeiten",8),("Reading comprehension",4)],
}
NAME = {'MA':'Mathematik','CH':'Chemie','BI':'Biologie','PH':'Physik','GE':'Geschichte','GG':'Geografie',
        'DE':'Deutsch','EN':'Englisch','EX':'Prüfung','AD':'Organisation','RE':'Repetition'}
TRACKS = {'NW':['CH','BI','PH'],'MA':['MA'],'GSW':['GE','GG'],'SPR':['DE','EN']}
TOTAL = {k: sum(h for _,h in v) for k,v in Q.items()}
TTOT = {t: sum(TOTAL[s] for s in subs) for t,subs in TRACKS.items()}

special = {D(2026,11,19):2.5, D(2026,12,24):1.5, D(2026,12,25):0, D(2026,12,26):2,
           D(2026,12,31):2, D(2027,1,1):0, D(2027,1,2):3}
holiday = {D(2026,12,24):'Heiligabend', D(2026,12,25):'Weihnachten', D(2026,12,26):'Stephanstag',
           D(2026,12,31):'Silvester', D(2027,1,1):'Neujahr', D(2027,1,2):'Berchtoldstag'}
def cap(d):
    if d in special: return special[d]
    return 7 if d.weekday()==6 else 5.5 if d.weekday()==5 else 5

START, CONTENT_END = D(2026,11,19), D(2027,2,7)
plan = {}   # date -> list of dict(subj, topic, h, done=False, note)
done_log = {D(2026,11,17):[('MA','Gleichungen: Einstieg, Vieta, erste Knacknüsse',2.5)],
            D(2026,11,18):[('MA','Gleichungen: Serien 1–3 gelöst',4.5)]}
for d,items in done_log.items():
    plan[d] = [dict(s=s,t=t,h=h,done=True) for s,t,h in items]

pos = {k:[0,0.0] for k in Q}  # topic index, hours consumed in topic
rem = dict(TOTAL)
alloc_track = {t:0.0 for t in TRACKS}
alloc_sub = {k:0.0 for k in Q}
finished = []  # (date, subj, topic)

def consume(subj, h, d):
    out = []
    while h > 1e-9 and pos[subj][0] < len(Q[subj]):
        i, used = pos[subj]
        name, th = Q[subj][i]
        take = min(h, th-used)
        out.append(dict(s=subj, t=name, h=take, part=(used>0 or take<th-used), first=(used==0)))
        pos[subj][1] += take; h -= take; rem[subj] -= take
        if pos[subj][1] >= th-1e-9:
            finished.append((d, subj, name)); pos[subj] = [i+1, 0.0]
    return out, h

cum = 0.0
d = START
while d <= CONTENT_END:
    c = cap(d)
    items = []
    if c > 0:
        cum += c
        # chunked allocation by deficit, 1h chunks (0.5 at the end)
        day_track = {}
        left = c
        while left > 1e-9:
            live = [t for t in TRACKS if any(rem[s]>1e-9 for s in TRACKS[t])]
            if not live: break
            tot_live = sum(sum(rem[s] for s in TRACKS[t]) for t in live)
            # deficit relative to remaining-work share
            def deficit(t):
                return TTOT[t]/sum(TTOT.values())*cum - alloc_track[t]
            t = max(live, key=deficit)
            chunk = 1.0 if left >= 1 else left
            if t == 'SPR' and day_track.get(t,0) >= 1.0 and len(live) > 1:
                t = max([x for x in live if x!='SPR'], key=deficit)
            day_track[t] = day_track.get(t,0) + chunk
            alloc_track[t] += chunk
            left -= chunk
        # map track hours to one sub-subject per day (by deficit)
        for t, h in day_track.items():
            subs = [s for s in TRACKS[t] if rem[s]>1e-9]
            s = max(subs, key=lambda s: TOTAL[s]/TTOT[t]*sum(alloc_sub[x] for x in TRACKS[t]) + TOTAL[s]/TTOT[t]*h - alloc_sub[s])
            alloc_sub[s] += h
            out, h2 = consume(s, h, d)
            while h2 > 1e-9:
                subs = [x for x in TRACKS[t] if rem[x]>1e-9]
                if not subs: break
                o2, h2 = consume(subs[0], h2, d); alloc_sub[subs[0]] += 0; out += o2
            items += out
    plan[d] = items
    d += ONE

leftover = {k:v for k,v in rem.items() if v>1e-9}

# ---------- admin tasks ----------
admin = {
 D(2026,11,19):["Bücher bestellen (3 Deutsch, 3 Englisch)","Rechner FX-82 Solar oder TI-30 ECO RS + Fundamentum kaufen"],
 D(2026,11,20):["Online anmelden: ganze Prüfung, Englisch"],
 D(2026,11,23):["Archivzugang alte Prüfungen beim SBFI anfragen"],
 D(2026,12,1):["Letzter Anmeldetag, 24:00"],
 D(2026,12,2):["Dossier per A-Post ans SBFI (spätestens heute)"],
 D(2026,12,22):["Rechnung bezahlt? (CHF 700)"],
}

# ---------- exam training phase ----------
train = {
 D(2027,2,8):[('MA','Probeprüfung Mathematik, 3 h unter Prüfungsbedingungen',3),('MA','Korrektur und Fehler nachlernen',1.5)],
 D(2027,2,9):[('CH','Probeprüfung Naturwissenschaften, 3 × 80 min',4),('BI','Korrektur und Fehler nachlernen',1)],
 D(2027,2,10):[('GE','Probeprüfung Geschichte und Geografie, 2 × 2 h',4),('GG','Korrektur und Fehler nachlernen',1)],
 D(2027,2,11):[('DE','Probeaufsatz Deutsch, 4 h',4),('DE','Korrektur',0.5)],
 D(2027,2,12):[('EN','Probeprüfung Englisch, 3 h',3),('EN','Korrektur',1)],
 D(2027,2,13):[('RE','Schwachstellen aus den Probeprüfungen',3)],
 D(2027,2,14):[('RE','Nur Formelblätter durchsehen, Material packen, früh schlafen',0.5)],
}
for d,items in train.items(): plan[d] = [dict(s=s,t=t,h=h) for s,t,h in items]
for i in range(5):
    d = D(2027,2,15)+i*ONE
    plan[d] = [dict(s='EX',t='Schriftliche Prüfung (Fach laut Aufgebot)',h=0,exam=True),
               dict(s='RE',t='Abends: Formelblatt des nächsten Fachs',h=0.5)]
plan[D(2027,2,20)] = [dict(s='RE',t='Frei',h=0)]
plan[D(2027,2,21)] = [dict(s='RE',t='Frei',h=0)]
oral_cycle = [('DE','Mündlich: Dürrenmatt und Storm wiederholen',2),('EN','Mündlich: Werk 1 und 2 präsentieren üben',2),
              ('MA','Mündlich: Sätze und Herleitungen laut erklären',2),('DE','Mündlich: Bühler und Burkart-Gedichte',2),
              ('EN','Mündlich: Werk 3, freies Sprechen',2),('MA','Mündlich: Theorie Analysis und Vektoren',2)]
d = D(2027,2,22); k = 0
while d <= D(2027,3,7):
    if d.weekday()==6:
        plan[d] = [dict(s='DE',t='Probe-Mündliche Deutsch (15 min laut, mit Uhr)',h=1),
                   dict(s='EN',t='Probe-Mündliche Englisch',h=1),dict(s='MA',t='Probe-Mündliche Mathematik',h=1)]
    else:
        s,t,h = oral_cycle[k%6]; s2,t2,h2 = oral_cycle[(k+1)%6]; k += 2
        plan[d] = [dict(s=s,t=t,h=h),dict(s=s2,t=t2,h=1)]
    d += ONE
for i in range(4):
    d = D(2027,3,8)+i*ONE
    plan[d] = [dict(s='EX',t='Mündliche Prüfungen, Pfäffikon SZ (Tag laut Aufgebot)',h=0,exam=True),
               dict(s='RE',t='Vorher: Werk-Notizen und Formeln kurz durchsehen',h=0.5)]
for i in range(3):
    plan[D(2027,3,12)+i*ONE] = [dict(s='RE',t='Geschafft. Auf den Entscheid warten.',h=0)]

json.dump(dict(leftover=leftover, finished=[(str(a),b,c) for a,b,c in finished]), open('state.json','w'), ensure_ascii=False, indent=1)
print('leftover', leftover)
print('content hours', sum(TOTAL.values()))

# ---------- HTML ----------
WD = ['Mo','Di','Mi','Do','Fr','Sa','So']
def fmt(h):
    return (f"{h:.1f}".rstrip('0').rstrip('.')).replace('.',',') + ' h'
first_exam = D(2027,2,15)

def item_html(it):
    s = it['s']; cls = s.lower()
    if it.get('exam'):
        return f'<div class="it exam"><span class="tg">Prüfung</span><span class="tp">{html.escape(it["t"])}</span></div>'
    h = f'<span class="hh">{fmt(it["h"])}</span>' if it['h'] > 0 else ''
    box = '<span class="cb done">✓</span>' if it.get('done') else ('<span class="cb"></span>' if it['h']>0 else '')
    tag = NAME[s]
    extra = ''
    if it.get('part') and not it.get('done'):
        extra = '<span class="pt">Start</span>' if it.get('first') else '<span class="pt">weiter</span>'
    return f'<div class="it {cls}">{box}<div class="tx"><span class="tg">{tag}</span>{extra}<span class="tp">{html.escape(it["t"])}</span></div>{h}</div>'

# finished topics by date for weekly footer
fin_by_week = {}
for d,s,t in finished:
    wk = d - (d.weekday())*ONE
    fin_by_week.setdefault(wk, []).append((s,t))

# cumulative soll per subject at end of each week
def soll_until(endd):
    acc = {k:0.0 for k in Q}
    for d,items in plan.items():
        if d <= endd and d >= START:
            for it in items:
                if it['s'] in acc and not it.get('done') and d <= CONTENT_END: acc[it['s']] += it['h']
    return acc

pages = []
wk = D(2026,11,16)
weekno = 0
while wk <= D(2027,3,8):
    weekno += 1
    days = [wk + i*ONE for i in range(7)]
    tot = sum(it['h'] for d in days for it in plan.get(d,[]) if not it.get('done'))
    donet = sum(it['h'] for d in days for it in plan.get(d,[]) if it.get('done'))
    end = days[-1]
    left_days = (first_exam - end).days
    cols = []
    for d in days:
        its = plan.get(d)
        dh = sum(it['h'] for it in (its or []))
        hol = holiday.get(d,'')
        if its is None:
            body = '<div class="empty">vor dem Start</div>'
        else:
            body = ''.join(item_html(it) for it in its) or '<div class="empty">frei</div>'
        ad = ''.join(f'<div class="ad"><span class="cb"></span><span>{html.escape(a)}</span></div>' for a in admin.get(d,[]))
        today = ' today' if d == START else ''
        sun = ' sun' if d.weekday()==6 else ''
        holc = ' hol' if hol else ''
        dhs = fmt(dh) if dh>0 else '–'
        cols.append(f'''<div class="day{sun}{holc}{today}"><div class="dh"><span class="wd">{WD[d.weekday()]}</span><span class="dt">{d.day}.{d.month}.</span><span class="dsum">{dhs}</span></div>{f'<div class="hl">{hol}</div>' if hol else ''}{'<div class="hl">ab 12 Uhr</div>' if d.weekday()==6 and not hol and its and dh>=5 else ''}{ad}{body}</div>''')
    # phase label
    if end < D(2027,2,8): phase = 'Lernphase'
    elif end <= D(2027,2,14): phase = 'Prüfungstraining'
    elif end <= D(2027,2,21): phase = 'Schriftliche Prüfungen'
    elif end <= D(2027,3,7): phase = 'Vorbereitung mündliche Prüfungen'
    else: phase = 'Mündliche Prüfungen'
    # footer
    fin = fin_by_week.get(wk, [])
    finhtml = ' · '.join(f'<b class="c-{s.lower()}">{NAME[s]}</b> {html.escape(t)}' for s,t in fin) or 'keine Themen-Abschlüsse diese Woche'
    acc = soll_until(end)
    bars = ''
    if end <= CONTENT_END + 6*ONE:
        for s in ['MA','CH','BI','PH','GE','GG','DE','EN']:
            pct = min(100, round(100*acc[s]/TOTAL[s]))
            bars += f'<div class="bar"><span class="bl">{NAME[s]}</span><span class="track"><span class="fill c-{s.lower()}bg" style="width:{pct}%"></span></span><span class="bp">{pct} %</span></div>'
    cd = f'{left_days} ' + ('Tag' if left_days==1 else 'Tage') + ' bis zur ersten schriftlichen Prüfung' if left_days > 0 else ('Prüfungswoche' if phase=='Schriftliche Prüfungen' else '')
    hours_line = f'Soll diese Woche: <b>{fmt(tot)}</b>' + (f' · bereits erledigt: <b>{fmt(donet)}</b>' if donet else '')
    pages.append(f'''<section class="page">
<header class="wh"><div><div class="ey">Woche {weekno} · {phase}</div><h2>{days[0].day}.{days[0].month}. – {end.day}.{end.month}.{end.year}</h2></div>
<div class="meta"><div>{hours_line}</div><div class="cd">{cd}</div></div></header>
<div class="grid">{''.join(cols)}</div>
<footer class="wf"><div class="fin"><div class="fl">Themen, die diese Woche fertig werden</div><div>{finhtml}</div></div>
{f'<div class="bars"><div class="fl">Soll-Stand Ende Woche (Anteil des Stoffs)</div>{bars}</div>' if bars else ''}</footer>
</section>''')
    wk += 7*ONE

# cover
weeks_tbl = ''
wk = D(2026,11,16); n=0; cumh=0
while wk <= D(2027,2,14):
    n+=1; days=[wk+i*ONE for i in range(7)]
    h = sum(it['h'] for d in days for it in plan.get(d,[]) if not it.get('done'))
    cumh += h
    weeks_tbl += f'<tr><td>{n}</td><td>{days[0].day}.{days[0].month}. – {days[-1].day}.{days[-1].month}.</td><td>{fmt(h)}</td><td>{fmt(cumh)}</td></tr>'
    wk += 7*ONE
sub_tbl = ''.join(f'<tr><td><span class="sw c-{s.lower()}bg"></span>{NAME[s]}</td><td>{len(Q[s])}</td><td>{fmt(TOTAL[s])}</td></tr>' for s in ['MA','CH','BI','PH','GE','GG','DE','EN'])
cover = f'''<section class="page cover">
<div class="ey">Passerelle Wintersession 2027 · Selbststudium</div>
<h1>Wochenplan bis zur Prüfung</h1>
<div class="cgrid">
<div>
<h3>Fixe Termine</h3>
<table class="ct"><tr><td>1. Dez. 2026, 24:00</td><td>Anmeldeschluss online</td></tr>
<tr><td>2. Dez. 2026</td><td>Dossier per A-Post ans SBFI</td></tr>
<tr><td><b>15.–19. Feb. 2027</b></td><td><b>Schriftliche Prüfungen, Zürich</b> (erster möglicher Tag: Mo 15. Feb.)</td></tr>
<tr><td>8.–11. März 2027</td><td>Mündliche Prüfungen Deutsch, Englisch, Mathematik, Pfäffikon SZ</td></tr></table>
<p class="sm">Daten der Prüfungstage aus der Recherche, genaue Tage und Fächerreihenfolge stehen im Aufgebot.</p>
<h3>So liest du den Plan</h3>
<ul class="sm">
<li>Pro Tag stehen Fach, Thema und Stunden. <b>Wann</b> du sie am Tag machst, entscheidest du.</li>
<li>Werktage 5 h, Samstag 5,5 h, Sonntag 7 h ab 12 Uhr. Feiertage reduziert, 25. Dez. und 1. Jan. frei.</li>
<li>„Start“ und „weiter“: Ein Thema läuft über mehrere Tage. Abhaken, wenn die Stunden gemacht sind.</li>
<li>Unten auf jeder Seite: welche Themen fertig sein sollten und der Soll-Stand pro Fach. Liegst du hinten, hol es am nächsten Sonntag nach.</li>
<li>Lernphase bis So 7. Feb., dann eine Woche Probeprüfungen, dann Prüfung.</li>
</ul>
<h3>Bisher: Thema Gleichungen</h3>
<p class="sm">Rekonstruiert aus den Zeiten der gespeicherten Lernschritte (deine Nachrichtenzeiten sehe ich nicht):
Di 17.11. ca. 14:40–16:00 plus eine Abendrunde, ≈ 2,5 h · Mi 18.11. Serie 1 am Vormittag und Serien 2–3 von 14:15–17:20, ≈ 4,5 h ·
<b>Total ≈ 7 h</b>, davon etwa 1 h 40 min für die 20 Aufgaben des Abschlusstests. Bleiben 3 h für Basiswechsel und Schwachstellen, sie stehen ab Do 19.11. im Plan.</p>
</div>
<div>
<h3>Stoff pro Fach</h3>
<table class="ct"><tr><th>Fach</th><th>Themen</th><th>Stunden</th></tr>{sub_tbl}
<tr><td><b>Total Lernphase</b></td><td><b>{sum(len(v) for v in Q.values())}</b></td><td><b>{fmt(sum(TOTAL.values()))}</b></td></tr></table>
<p class="sm">Dazu ≈ 27 h Probeprüfungen (8.–14. Feb.) und ≈ 30 h mündliche Vorbereitung (22. Feb.–7. März).</p>
<h3>Soll-Stunden pro Woche</h3>
<table class="ct"><tr><th>Woche</th><th>Datum</th><th>Soll</th><th>kumuliert</th></tr>{weeks_tbl}</table>
</div></div>
</section>'''

css = open('plan.css').read()
doc = f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Wochenplan Passerelle</title><style>{css}</style></head><body>{cover}{"".join(pages)}<script>document.body.dataset.ready="1"</script></body></html>'
open('plan.html','w').write(doc)
print('pages', len(pages)+1)
