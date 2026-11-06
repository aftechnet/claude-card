"""Lint an AFTECH decision card (v3). Usage: python3 card_lint.py card.html ..."""
import re, sys

PIN = re.compile(r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/gh/aftechnet/claude-card@[0-9a-f]{40}/card\.css">')

JARGON = {"git","merge","mr","commit","deploy","ct","claim","kb","hash","sha","api","repo","pr","sql"}

def v15_checks(html: str) -> list[str]:
    """v1.5: short sentences, true-scale bars, card id on change buttons, one doubt line."""
    errs = []
    vis = re.sub(r"<details>.*?</details>|<h2 class=\"sr-only\">.*?</h2>|onclick=\"[^\"]*\"", "", html, flags=re.S)
    for frag in re.split(r"<[^>]+>", vis):
        for sent in re.split(r"[.!?](?:\s|$)|\u00b7", frag):
            n = len(re.findall(r"[\w%'/-]+", sent))
            if n > 15: errs.append(f"sentence over 15 words ({n}): {sent.strip()[:40]}")
    for w, txt in re.findall(r'<div class="[a-z]+" style="width:(\d+(?:\.\d+)?)%">([^<]*)</div>', html):
        m = re.search(r"(\d+(?:\.\d+)?)\s*of\s*(\d+(?:\.\d+)?)", txt) or re.fullmatch(r"\s*(\d+(?:\.\d+)?)%\s*", txt)
        if not m: continue
        want = float(m.group(1)) / float(m.group(2)) * 100 if m.lastindex == 2 else float(m.group(1))
        if abs(float(w) - want) > 2: errs.append(f"bar width {w}% does not match its number '{txt.strip()}' ({want:.0f}%)")
    for btn in re.findall(r'<button class="o[^"]*"[^>]*>.*?</button>', html, re.S):
        if "Changes now" in btn and not re.search(r"sendPrompt\('[^']*#\w+[^']*'\)", btn):
            errs.append("change button without card id: send 'yes NAME #HHMM'")
    if html.count('class="dbt"') > 1: errs.append("more than one doubt line")
    return errs

def lint(html: str) -> list[str]:
    errs = []
    if not PIN.search(html): errs.append("no pinned card.css link")
    if "<style" in html: errs.append("has <style> block")
    folds = re.findall(r"<details>.*?</details>", html, re.S)
    vis_len = len(re.sub(r"<details>.*?</details>", "", html, flags=re.S))
    if vis_len > 1100: errs.append(f"too long: {vis_len} > 1100 (fold not counted)")
    if any(len(f) > 500 for f in folds): errs.append("fold too long: > 500")
    if len(folds) > 1: errs.append("more than one fold")
    if re.search(r"sendPrompt\('yes'\)", html): errs.append("warn: bare 'yes' button: name the card ('yes cut plan')")
    errs += v15_checks(html)
    if "→" not in html and 'class="bar"' not in html: errs.append("no flow arrow or bars")
    btns = re.findall(r'<button class="o( p)?"[^>]*>(.*?)</button>', html, re.S)
    if not btns: errs.append("no option buttons")
    if len(btns) > 4: errs.append(f"{len(btns)} options > 4")
    if any(p for p, _ in btns[1:]): errs.append("main option (o p) not first")
    for p in re.findall(r"sendPrompt\('([^']*)'\)", html):
        if p.rstrip().endswith(":") or not p.strip(): errs.append(f"half-filled button: '{p}'")
    for _, body in btns:
        if "Show details" not in body and "<small>" not in body:
            errs.append("option without 'what happens next' line")
    if re.search(r'class="(t )?r"', html): errs.append("warn: red used (only for can't-undo)")
    if 'class="t ' in html and 'class="s"' not in html: errs.append("live change without Not touched / Undo line (class s)")
    if "Live ·" in html: errs.append("old tag wording: use Changes now · low/medium/high risk")
    vis = re.sub(r"<[^>]+>", " ", re.sub(r"<h2 class=\"sr-only\">.*?</h2>|onclick=\"[^\"]*\"", "", html))
    jar = sorted({w for w in re.findall(r"[A-Za-z]+", vis) if w.lower() in JARGON})
    if jar: errs.append("warn: tech words on card: " + ", ".join(jar))
    return errs

if __name__ == "__main__":
    bad = 0
    for f in sys.argv[1:]:
        e = lint(open(f, encoding="utf-8").read())
        print(f, "OK" if not e else "; ".join(e)); bad += bool([x for x in e if not x.startswith("warn")])
    sys.exit(1 if bad else 0)
