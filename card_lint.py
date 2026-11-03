"""Lint an AFTECH decision card (v3). Usage: python3 card_lint.py card.html ..."""
import re, sys

PIN = re.compile(r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/gh/aftechnet/claude-card@[0-9a-f]{40}/card\.css">')

JARGON = {"git","merge","mr","commit","deploy","ct","claim","kb","hash","sha","api","repo","pr","sql"}

def lint(html: str) -> list[str]:
    errs = []
    if not PIN.search(html): errs.append("no pinned card.css link")
    if "<style" in html: errs.append("has <style> block")
    if len(html) > 1100: errs.append(f"too long: {len(html)} > 1100")
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
